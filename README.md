# Student Management API
A production-grade REST API built with FastAPI and MongoDB featuring JWT Authentication, Role Based Access Control, Pagination, and Filtering.

## Features
- JWT Authentication (AccessTokens)
- Role Based Access Control (Admin & User)
- Full CRUD for Students
- Pagination & Filtering
- Sorting & Search
- Active User Check
- Error Handling

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python     | Programming language |
| FastAPI    | Web framework |
| MongoDB    | Database |
| PyJWT      | JWT token generation |
| Bcrypt     | Password hashing |
| Pydantic   | Data validation |
| Python Dotenv | Environment variables |

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

### Auth Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register user |
| POST | /api/v1/auth/login | Login user |
| POST | /api/v1/auth/logout | Logout user |
| GET  | /api/v1/auth/me | Get profile |


### Student Routes (Protected)

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/api/v1/students` | Admin, User | Get all students |
| GET | `/api/v1/students/{id}` | Admin, User | Get single student |
| GET | `/api/v1/students/search/{course}` | Admin, User | Search by course |
| POST | `/api/v1/students` | Admin only | Create student |
| PUT | `/api/v1/students/{id}` | Admin only | Update student |
| DELETE | `/api/v1/students/{id}` | Admin only | Delete student |

---

## Project Structure
```
student-api/
├── main.py            → App entry point
├── database.py        → MongoDB connection
├── models.py          → Pydantic models
├── routes.py          → Student CRUD routes
├── auth.py            → JWT & role logic
├── auth_routes.py     → Auth endpoints
├── pagination.py      → Pagination & filter logic
├── requirements.txt   → Dependencies
├── .env               → Environment variables (not pushed)
├── .gitignore         → Git ignore rules
└── README.md          → Project documentation
```
## Pagination & Filtering

The `GET /api/v1/students` endpoint supports the following query parameters:

### Pagination

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `per_page` | int | 10 | Students per page (max 100) |

### Filtering

| Parameter | Type | Description |
|---|---|---|
| `course` | string | Filter by course name |
| `grade` | string | Filter by grade |
| `min_age` | int | Minimum age |
| `max_age` | int | Maximum age |
| `search` | string | Search by name or email |

### Sorting

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sort_by` | string | name | Sort by: name, age, course, grade |
| `order` | string | asc | Order: asc or desc |

## Authentication Flow
```
1. Register  →  POST /api/v1/auth/register
2. Login     →  POST /api/v1/auth/login  →  get access_token + refresh_token
3. Request   →  Add header: Authorization: Bearer <access_token>
4. Expired   →  POST /api/v1/auth/refresh  →  get new access_token
5. Logout    →  POST /api/v1/auth/logout  →  token blacklisted
```

---
## Future Improvements

- [ ] Logging & Rate Limiting
- [ ] Email Verification on Register
- [ ] Password Reset via Email
- [ ] Export Students to CSV/Excel
- [ ] File Upload for Student Profile Photo
- [ ] Unit Testing
- [ ] Docker Support
- [ ] Deploy to Railway/Render
- [ ] CI/CD Pipeline

---

## Author

**Mayur** — [github.com/pmayur1997](https://github.com/pmayur1997)

---

## License

This project is open source and available under the [MIT License](LICENSE).