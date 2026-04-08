from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import user_collection
from dotenv import load_dotenv
from bson import ObjectId
import bcrypt, jwt, os, smtplib, secrets, resend
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL    = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
APP_BASE_URL = os.getenv("APP_BASE_URL")
resend.api_key = os.environ.get("RESEND_API_KEY")
security = HTTPBearer()

# ── Hash password ────────────────────────────────
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# ── Verify password ──────────────────────────────
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

# ── Create JWT token ─────────────────────────────
def create_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ── Decode & verify token ────────────────────────
def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

#── Create a secure email verification token ────────────────────────
def create_verification_token()->str:
    return secrets.token_urlsafe(32)

#── Share SMTP Sender────────────────────────────────────────────────
def send_email(to_email: str, subject: str, text_body: str, html_body: str ):
    """message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"]    = SMTP_EMAIL
    message["To"]      = to_email
 
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))"""
 
    try:
        email = resend.Emails.send({
            "from": "Acme <onboarding@resend.dev>",  # Use your verified domain here
            "to": [to_email],
            "subject": subject,
            "text":f"text_body",
            "html": f"text_html",
        })
        return {"status": "success", "email_id": email["id"]}
        """with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, message.as_string())"""
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
    
# ── Send verification email via Gmail SMTP ───────
def send_verification_email(to_email: str, token: str):
    verify_url = f"{APP_BASE_URL}/api/v1/auth/verify-email?token={token}"
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email — Student API"
    message["From"]    = SMTP_EMAIL
    message["To"]      = to_email
    """
    # Plain text fallback
    text_body = f"""
Hi,
 
Please verify your email address by clicking the link below:
 
{verify_url}
 
This link expires in 24 hours.
 
If you did not register, ignore this email.
"""
 
    # HTML body
    html_body = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 40px;">
  <div style="max-width: 480px; margin: auto; background: white; border-radius: 8px; padding: 32px;">
    <h2 style="color: #1a1a1a; margin-bottom: 8px;">Verify your email</h2>
    <p style="color: #555; font-size: 15px; line-height: 1.6;">
      Thanks for registering with the Student Management API.
      Click the button below to verify your email address.
    </p>
    <a href="{verify_url}"
       style="display: inline-block; margin: 24px 0; padding: 12px 28px;
              background: #4f46e5; color: white; text-decoration: none;
              border-radius: 6px; font-size: 15px; font-weight: 500;">
      Verify Email
    </a>
    <p style="color: #999; font-size: 13px;">
      This link expires in <strong>24 hours</strong>.<br>
      If you did not register, you can safely ignore this email.
    </p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
    <p style="color: #bbb; font-size: 12px;">Student Management API</p>
  </div>
</body>
</html>
"""
    send_email(to_email, "Verify your email — Student API", text_body, html_body)

# ── Password reset email via Gmail SMTP ───────    
def send_password_reset_email(to_email: str, token: str):
    verify_url = f"{APP_BASE_URL}/api/v1/auth/reset-password?token={token}"
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset your password — Student API"
    message["From"]    = SMTP_EMAIL
    message["To"]      = to_email
    """
    # Plain text fallback
    text_body = f"""
Hi,
 
We received a request to reset your password. Click the link below to set a new one:
 
{verify_url}
 
This link expires in 24 hours.
 
If you did not register, ignore this email.
"""
 
    # HTML body
    html_body = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 40px;">
  <div style="max-width: 480px; margin: auto; background: white; border-radius: 8px; padding: 32px;">
    <h2 style="color: #1a1a1a; margin-bottom: 8px;">Verify your email</h2>
    <p style="color: #555; font-size: 15px; line-height: 1.6;">
      Thanks for registering with the Student Management API.
      Click the button below to verify your email address.
    </p>
    <a href="{verify_url}"
       style="display: inline-block; margin: 24px 0; padding: 12px 28px;
              background: #4f46e5; color: white; text-decoration: none;
              border-radius: 6px; font-size: 15px; font-weight: 500;">
      Reset Password
    </a>
    <p style="color: #999; font-size: 13px;">
      This link expires in <strong>24 hours</strong>.<br>
      If you did not register, you can safely ignore this email.
    </p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
    <p style="color: #bbb; font-size: 12px;">Student Management API</p>
  </div>
</body>
</html>
"""
    send_email(to_email, "Reset your password — Student API", text_body, html_body)

# ── Get current logged-in user (dependency) ──────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    
    user = user_collection.find_one({"_id": ObjectId(payload.get("user_id"))})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }
def require_role(*roles:str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {list(roles)}"
            )
        return current_user
    return role_checker

# ── Shortcut dependencies ────────────────────────
require_admin = require_role("admin")
require_user  = require_role("admin", "user")   # both can access