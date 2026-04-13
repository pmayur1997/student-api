src/
├── api/
│   └── axios.js              → axios instance with base URL + auth header
├── context/
│   └── AuthContext.jsx       → global auth state (token, user, role)
├── components/
│   ├── Navbar.jsx            → top nav with logout
│   ├── ProtectedRoute.jsx    → redirect if not logged in
│   └── AdminRoute.jsx        → redirect if not admin
├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── VerifyEmail.jsx
│   ├── ForgotPassword.jsx
│   ├── ResetPassword.jsx
│   ├── Dashboard.jsx         → student list, search, filter, export
│   ├── CreateStudent.jsx
│   └── EditStudent.jsx
├── App.jsx                   → all routes defined here
├── index.css                 → tailwind directives
└── main.jsx                  → entry point