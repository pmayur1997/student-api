from fastapi import APIRouter, HTTPException, Depends , Query, Request
from bson import ObjectId
from database import student_collection
from models import StudentModel, UpdateStudentModel
from auth import require_admin, require_user, get_current_user
from pagination import paginate, build_filter_query
from typing import Optional
from limiter import check_limit
from logger import logger

router = APIRouter()

def format_student(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "age": student["age"],
        "course": student["course"],
        "grade": student.get("grade", "N/A")
    }

#CREATE — Admin Only
@router.post("/students", status_code=201)
async def create_student(request: Request,student: StudentModel, current_user: dict = Depends(require_admin)):
    check_limit(request, "register", max_requests=5)
    if student_collection.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    result = student_collection.insert_one(student.dict())
    logger.info(f"Student created | id: {result.inserted_id} | by: {current_user['email']}")
    return {"message": "Student created", "id": str(result.inserted_id)}

#GET ALL — Admin & user
@router.get("/students")
async def get_all_students(
    request: Request,
    # Pagination params
    page:     int = Query(default=1,  ge=1,   description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Students per page"),

    # Filter params
    course:   Optional[str] = Query(default=None, description="Filter by course"),
    grade:    Optional[str] = Query(default=None, description="Filter by grade"),
    min_age:  Optional[int] = Query(default=None, ge=1,  description="Minimum age"),
    max_age:  Optional[int] = Query(default=None, ge=1,  description="Maximum age"),
    search:   Optional[str] = Query(default=None, description="Search by name or email"),

    # Sorting params
    sort_by:  str = Query(default="name", description="Sort by field: name, age, course, grade"),
    order:    str = Query(default="asc",  description="Order: asc or desc"),

    current_user: dict = Depends(require_user)
    ):
    check_limit(request, "getstudents", max_requests=100)
     # Build filter query
    query = build_filter_query(
        course=course,
        grade=grade,
        min_age=min_age,
        max_age=max_age,
        search=search
    )

    # Sorting
    sort_order = 1 if order == "asc" else -1
    allowed_sort_fields = ["name", "age", "course", "grade"]
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {allowed_sort_fields}")

    # Fetch from MongoDB with filter and sort
    students = list(
        student_collection.find(query).sort(sort_by, sort_order)
    )

    # Format all students
    formatted = [format_student(s) for s in students]

    # Apply pagination
    result = paginate(formatted, page, per_page)
    result["filters_applied"] = {
        "course":  course,
        "grade":   grade,
        "min_age": min_age,
        "max_age": max_age,
        "search":  search,
        "sort_by": sort_by,
        "order":   order
    }
    logger.info(f"Students fetched | page: {page} | filters: {query} | by: {current_user['email']}")
    return {
        "message": "Students fetched",
        "requested_by": current_user["username"],
        "role": current_user["role"],
        "data": result
    }

#GET ONE — Admin and user
@router.get("/students/{student_id}")
async def get_student(request: Request,student_id: str, current_user: dict = Depends(require_user)):
    check_limit(request, "get_Student", max_requests=5)
    try:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    logger.info(f"Student fetched | id: {student_id} | by: {current_user['email']}")
    return {"message": "Student fetched", "data": format_student(student)}

#UPDATE — Admin only
@router.put("/students/{student_id}")
async def update_student(request:Request, student_id: str, update_data: UpdateStudentModel, current_user: dict = Depends(require_admin)):
    check_limit(request, "update_student", max_requests=20)
    update_fields = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    try:
        result = student_collection.update_one(
            {"_id": ObjectId(student_id)}, {"$set": update_fields}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    logger.info(f"Student updated | id: {student_id} | by: {current_user['email']}")
    return {"message": "Student updated by admin {current_user['username']}"}

#DELETE — Admin
@router.delete("/students/{student_id}")
async def delete_student(request:Request, student_id: str, current_user: dict = Depends(require_admin)):
    check_limit(request, "delete_student", max_requests=10)
    try:
        result = student_collection.delete_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    logger.info(f"Student deleted | id: {student_id} | by: {current_user['email']}")
    return {"message": "Student deleted by admin {current_user['username']}"}

#SEARCH — Admin and User
@router.get("/students/search/{course}")
def search_by_course(
    request: Request,
    course: str,
    page:     int = Query(default=1,  ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(require_user)
    ):
    check_limit(request, "search_students", max_requests=5)
    students = list(student_collection.find({"course": {"$regex": course, "$options": "i"}}))
    result = [format_student(s) for s in students]
    if not result:
        raise HTTPException(status_code=404, detail="No students found")
    logger.info(f"Search by course | course: {course} | by: {current_user['email']}")
    return paginate(result,page,per_page)