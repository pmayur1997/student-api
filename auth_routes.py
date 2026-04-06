from fastapi import APIRouter, HTTPException, Depends, Request
from database import user_collection,email_tokens_collection
from models import RegisterModel, LoginModel
from auth import (
    hash_password, verify_password, create_token, get_current_user,
    decode_token,create_verification_token,send_verification_email)
from datetime import datetime, UTC , timedelta
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
    result = user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed,
        "role":user.role,
        "is_Active":True,
        "is_Verified":False,
        "created_At": datetime.utcnow()
    })
    # Create & store verification token (expires in 24 hours)
    token = create_verification_token()
    expires = datetime.utcnow() + timedelta(hours=24)
    email_tokens_collection.insert_one(
        {
        "user_id":    result.inserted_id,
        "token":      token,
        "expires_at": expires,
        "used":       False 
        }
    )
    send_verification_email(user.email, token)
    logger.info(f"User registered successfully | {user.email} | role: {user.role} | verification email sent.")
    return {"message": "User registered successfully . Please check the email for verification."}

# Verify Email 
@router.post("/verify-email")
async def verify_email(token:str):
    #Find token record
    token_record = email_tokens_collection.find_one({"token":token})
    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid verification link")
    if token_record.get("used"):
        raise HTTPException(status_code=400, detail="Link has been used already")
    if datetime.utcnow() > token_record["expires_at"]:
        raise HTTPException(status_code=400,
                            detail=" Verification link has expired. Request for the new one.")
    # Mark User as Verified
    user_collection.update_one(
        {"_id": token_record["user_id"]},
        {"$set":{"is_Verified":True}}
    )

    #Mark Token as used
    email_tokens_collection.update_one(
        {"_id": token_record["_id"]},
        {"$set":{"used":True}}
    )
    logger.info(f"Email verified | user_id: {token_record['user_id']}")
    return {"message": "Email verified successfully. You can now log in."}

# Resend Verification Email
@router.post("/resend-verification")
async def resend_verification(request:Request, email:str):
    check_limit(request,"resend_verification", max_requests=5)
    user = user_collection.find_one({"email":email})
    if not user:
        # Don't reveal whether the email exists
        return {"message": "If that email is registered, a verification link has been sent."}
    if user.get("is_Verified"):
        raise HTTPException(status_code=400,
                            detail="The account is already verified")
    # Invalidate all previous tokens for this user
    email_tokens_collection.update_many(
        {"user_id": user["_id"], "used": False},
        {"$set": {"used": True}}
    )
    # Create new token
    token   = create_verification_token()
    expires = datetime.utcnow() + timedelta(hours=24)
    email_tokens_collection.insert_one({
        "user_id":    user["_id"],
        "token":      token,
        "expires_at": expires,
        "used":       False
    })
    send_verification_email(email, token)
    logger.info(f"Verification email resent | email: {email}")
    return {"message": "If that email is registered, a verification link has been sent."}


#LOGIN
@router.post("/login")

async def login(request:Request, user: LoginModel):
    check_limit(request, "login", max_requests=5)
    logger.info(f"Login attempt | email: {user.email}")
    found = user_collection.find_one({"email": user.email})

    if not found or not verify_password(user.password, found["password"]):
        logger.warning(f"Login failed | {user.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Block login if email is not verified
    if not found.get("is_Verified",False):
        logger.warning(f"Login Blocked | unverified email|{user.email}")
        raise HTTPException(status_code=403,
                            detail="Please verify your email before logging in. Check your inbox or request a new link at POST /api/v1/auth/resend-verification"
                            )
    user_id = str(found["_id"])
    role = found.get("role","user")
    token = create_token({
        "user_id": user_id , 
        "email": found["email"],
        "role": role
        })
    logger.info(f"Login Success | email: {user.email} | role: {role}")
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