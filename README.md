# Student Management API

A REST API built with FastAPI, MongoDB, and JWT Authentication.

## Features
- JWT Authentication (Access + Refresh Tokens)
- Role Based Access Control (Admin & User)
- Full CRUD for Students
- Search by Course

## Tech Stack
- Python
- FastAPI
- MongoDB
- JWT

## Installation

1. Clone the repository
   git clone https://github.com/your_username/student-api.git
   cd student-api

2. Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   MONGO_URI=mongodb://localhost:27017
   DB_NAME=studentdb
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7

5. Run the server
   uvicorn main:app --reload

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register user |
| POST | /api/v1/auth/login | Login user |
| POST | /api/v1/auth/logout | Logout user |
| GET  | /api/v1/auth/me | Get profile |

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/students | Get all students |
| GET | /api/v1/students/{id} | Get single student |
| POST | /api/v1/students | Create student |
| PUT | /api/v1/students/{id} | Update student |
| DELETE | /api/v1/students/{id} | Delete student |
| GET | /api/v1/students/search/{course} | Search by course |