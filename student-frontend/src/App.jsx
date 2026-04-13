import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute, AdminRoute } from "./components/ProtectedRoute";
 
import Login             from "./pages/Login";
import Register          from "./pages/Register";
import { VerifyEmail, ForgotPassword, ResetPassword } from "./pages/AuthPages";
import Dashboard         from "./pages/Dashboard";
import { CreateStudent, EditStudent } from "./pages/StudentForm";
 
const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
        <Routes>
          {/* Public routes */}
          <Route path="/login"            element={<Login />} />
          <Route path="/register"         element={<Register />} />
          <Route path="/verify-email"     element={<VerifyEmail />} />
          <Route path="/forgot-password"  element={<ForgotPassword />} />
          <Route path="/reset-password"   element={<ResetPassword />} />
 
          {/* Protected routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute><Dashboard /></ProtectedRoute>
          } />
 
          {/* Admin only routes */}
          <Route path="/students/create" element={
            <AdminRoute><CreateStudent /></AdminRoute>
          } />
          <Route path="/students/edit/:id" element={
            <AdminRoute><EditStudent /></AdminRoute>
          } />
 
          {/* Default redirect */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
 
export default App;