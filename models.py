from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# ── Student models ───────────────────────────────
class StudentModel(BaseModel):
    name: str
    email: str
    age: int
    course: str
    grade: Optional[str] = None

class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    grade: Optional[str] = None

# ── Role enum ────────────────────────────────────
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"

# ── Pagination Model ──────────────────────────────────
class PaginationParam(BaseModel):
    page: int = 1
    per_page: int = 10

# ── Filter Model ──────────────────────────────────
class StudentFilter(BaseModel):
    course:  Optional[str] = None
    grade:   Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    search:  Optional[str] = None    # search by name or email

# ── Auth models ──────────────────────────────────
class RegisterModel(BaseModel):
    username: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.user 

class LoginModel(BaseModel):
    email: str
    password: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str

# ── Resend Verification ──────────────────────────────────
class ResendVerificationModel(BaseModel):
    email : str