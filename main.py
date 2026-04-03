from fastapi import FastAPI
from routes import router as student_router
from auth_routes import router as auth_router

app = FastAPI(
    title="Student Management API",
    description="A simple CRUD API using FastAPI and MongoDB",
    version="2.0.0"
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

# Student routes (protected)
app.include_router(student_router, prefix="/api/v1", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Welcome to Student Management API"}

##How the auth flow works
'''
1. Register   →  POST /api/v1/auth/register   →  creates account
2. Login      →  POST /api/v1/auth/login       →  returns JWT token
3. Use token  →  Add to every request header   →  access protected routes
'''