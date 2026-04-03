from pydantic import BaseModel
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