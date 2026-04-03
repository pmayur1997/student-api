from fastapi import APIRouter, HTTPException
from database import user_collection
from models import RegisterModel, LoginModel
from auth import hash_password, verify_password, create_token, get_current_user
from fastapi import Depends

router = APIRouter()

#REGISTER
@router.post("/register", status_code=201)
def register(user: RegisterModel):
    # Check if email already exists
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username already exists
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = hash_password(user.password)
    user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed
    })

    return {"message": "User registered successfully"}


#LOGIN
@router.post("/login")
def login(user: LoginModel):
    found = user_collection.find_one({"email": user.email})

    if not found or not verify_password(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"user_id": str(found["_id"]), "email": found["email"]})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


#GET current logged-in user profile
@router.get("/me")
def my_profile(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Profile fetched",
        "data": current_user
    }