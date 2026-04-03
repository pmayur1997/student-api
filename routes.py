from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import student_collection
from models import StudentModel, UpdateStudentModel
from auth import get_current_user
from auth import require_admin, require_user

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
def create_student(student: StudentModel, current_user: dict = Depends(require_admin)):
    if student_collection.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    result = student_collection.insert_one(student.dict())
    return {"message": "Student created", "id": str(result.inserted_id)}

#GET ALL — Admin & user
@router.get("/students")
def get_all_students(current_user: dict = Depends(require_user)):
    students = student_collection.find()
    return {
        "message": "Students fetched",
        "requested_by": current_user["username"],
        "role": current_user["role"],
        "data": [format_student(s) for s in students]
    }

#GET ONE — Admin and user
@router.get("/students/{student_id}")
def get_student(student_id: str, current_user: dict = Depends(require_user)):
    try:
        student = student_collection.find_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student fetched", "data": format_student(student)}

#UPDATE — Admin only
@router.put("/students/{student_id}")
def update_student(student_id: str, update_data: UpdateStudentModel, current_user: dict = Depends(require_admin)):
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
    return {"message": "Student updated by admin {current_user['username']}"}

#DELETE — Admin
@router.delete("/students/{student_id}")
def delete_student(student_id: str, current_user: dict = Depends(require_admin)):
    try:
        result = student_collection.delete_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted by admin {current_user['username']}"}

#SEARCH — Admin and User
@router.get("/students/search/{course}")
def search_by_course(course: str, current_user: dict = Depends(require_user)):
    students = student_collection.find({"course": {"$regex": course, "$options": "i"}})
    result = [format_student(s) for s in students]
    if not result:
        raise HTTPException(status_code=404, detail="No students found")
    return {"count": len(result), "data": result}