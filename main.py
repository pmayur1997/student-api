from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logger import logger
from routes import router as student_router
from auth_routes import router as auth_router
from export_routes import router as export_router
import time

app = FastAPI(
    title="Student Management API",
    description="FastAPI + MongoDB + JWT + RBAC + Pagination + Logging + Rate Limiting",
    version="3.0.0"
)
# ── Log every request ────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request  | {request.method} {request.url} | IP: {request.client.host}")
    response   = await call_next(request)
    duration   = round((time.time() - start_time) * 1000, 2)
    logger.info(f"Response | {request.method} {request.url} | Status: {response.status_code} | {duration}ms")
    return response

# ── Handle 429 globally ──────────────────────────
@app.exception_handler(429)
async def rate_limit_handler(request: Request, exc):
    logger.warning(f"Rate limit exceeded | IP: {request.client.host} | URL: {request.url}")
    return JSONResponse(
        status_code=429,
        content={
            "error":   "Too many requests",
            "message": "You have exceeded the request limit. Please try again later."
        }
    )

# ── Global exception handler ─────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error | {request.method} {request.url} | Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc)}
    )

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
# Student routes (protected)
app.include_router(student_router, prefix="/api/v1", tags=["Students"])
#Export Data routes
app.include_router(export_router,prefix="/api/v1/export",tags=["Export"])

@app.get("/")
def root():
    return {"message": "Welcome to Student Management API V3"}

##How the auth flow works
'''
1. Register   →  POST /api/v1/auth/register   →  creates account
2. Login      →  POST /api/v1/auth/login       →  returns JWT token
3. Use token  →  Add to every request header   →  access protected routes
'''