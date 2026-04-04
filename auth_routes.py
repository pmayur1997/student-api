from fastapi import APIRouter, HTTPException, Depends, Request
from database import user_collection
from models import RegisterModel, LoginModel
from auth import hash_password, verify_password, create_token, get_current_user,decode_token
from datetime import datetime, UTC
from limiter import check_limit
from logger import logger
from bson import ObjectId

router = APIRouter()

#REGISTER = Limit 5 per minute
@router.post("/register", status_code=201)
async def register(request:Request, user: RegisterModel):
    check_limit(request, "register", max_requests=5)
    logger.info(f"Register attempts | email: {user.email}")
    # Check if email already exists
    if user_collection.find_one({"email": user.email}):
        logger.warning(f"Register failed | Email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username already exists
    if user_collection.find_one({"username": user.username}):
        logger.warning(f"Register failed | Username taken: {user.username}")
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = hash_password(user.password)
    user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed,
        "role":user.role,
        "is_Active":True,
        "created_At": datetime.utcnow()
    })
    logger.info(f"User registered successfully | {user.email} | role: {user.role}")
    return {"message": "User registered successfully"}


#LOGIN
@router.post("/login")

async def login(request:Request, user: LoginModel):
    check_limit(request, "login", max_requests=5)
    logger.info(f"Login attempt | email: {user.email}")
    found = user_collection.find_one({"email": user.email})

    if not found or not verify_password(user.password, found["password"]):
        logger.warning(f"Login failed | {user.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user_id = str(found["_id"])
    role = found.get("role","user")
    token = create_token({
        "user_id": user_id , 
        "email": found["email"],
        "role": role
        })
    logger.info(f"Login Success | email: {user.email} | role: {user.role}")
    return {
        "message": "Login successful",
        "role":role,
        "access_token": token,
        "token_type": "bearer"
    }

#GET current logged-in user profile
@router.get("/me")
async def my_profile(request: Request, current_user: dict = Depends(get_current_user)):
    logger.info(f"Profile fetched: | user:{current_user['email']}")
    return {
        "message": "Profile fetched",
        "data": current_user
    }