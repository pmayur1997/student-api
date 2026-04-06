from fastapi import APIRouter,Query, Depends, Request,HTTPException
from fastapi.responses import StreamingResponse
from database import student_collection,user_collection
from auth import require_user, require_admin
from limiter import check_limit
from logger import logger
from datetime import datetime
import pandas as pd
import io

router=APIRouter()

# ── Helpers ───────────────────────────────────────
 
def df_to_csv(df: pd.DataFrame) -> StreamingResponse:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv"
    )

def df_to_excel(df: pd.DataFrame, sheet_name: str) -> StreamingResponse:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def make_response(df: pd.DataFrame, fmt: str, filename: str, sheet_name: str) -> StreamingResponse:
    if fmt == "csv":
        response = df_to_csv(df)
        ext = "csv"
    elif fmt == "excel":
        response = df_to_excel(df, sheet_name)
        ext = "xlsx"
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{filename}_{timestamp}.{ext}"'
    )
    return response

# ── EXPORT STUDENTS  ───────────────────────────────
# ──── Admin and User ───────────────────────────────
@router.get("/students")
async def export_students(
    request:Request, 
    format: str = Query(default="csv",description="Export format : csv or excel"),
    current_user: dict = Depends(require_user)):
    check_limit(request,"export_students",max_requests=10)
    if format not in ("csv","excel"):
        raise HTTPException(status_code= 400, detail= "The format must be 'CSV' or 'Excel'")
    students = list(student_collection.find())

    if not students:
        data = []
    else:
        data = [
            {
                #"id":     str(s["_id"]),
                "name":   s.get("name", ""),
                "email":  s.get("email", ""),
                "age":    s.get("age", ""),
                "course": s.get("course", ""),
                "grade":  s.get("grade", "N/A"),
            }
            for s in students
        ]
    df = pd.DataFrame(data, columns=["name", "email", "age", "course", "grade"])
    logger.info(f"Students exported | format: {format} | count: {len(data)} | by: {current_user['email']}")
    return make_response(df, format, "students", "Students")      

# ── EXPORT USERS ──────────────────────────────────
# Admin and User
@router.get("/users")
async def export_users(
    request: Request,
    format: str = Query(default="csv", description="Export format: csv or excel"),
    current_user: dict = Depends(require_admin)
):
    check_limit(request, "export_users", max_requests=10)
 
    if format not in ("csv", "excel","pdf"):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="format must be 'csv' or 'excel'")
 
    users = list(user_collection.find())
 
    if not users:
        data = []
    else:
        data = [
            {
                #"id":          str(u["_id"]),
                "username":    u.get("username", ""),
                "email":       u.get("email", ""),
                "role":        u.get("role", ""),
                "is_verified": u.get("is_Verified", False),
                "is_active":   u.get("is_Active", True),
                "created_at":  u.get("created_At", "").strftime("%Y-%m-%d %H:%M:%S")
                               if u.get("created_At") else "",
            }
            for u in users
        ]
 
    df = pd.DataFrame(data, columns=[
        "username", "email", "role","is_verified", "is_active", "created_at"
    ])
 
    logger.info(f"Users exported | format: {format} | count: {len(data)} | by: {current_user['email']}")
    return make_response(df, format, "users", "Users")