import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
 
export const ProtectedRoute = ({ children }) => {
  const { token, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center h-screen text-gray-500">Loading...</div>;
  return token ? children : <Navigate to="/login" replace />;
};
 
export const AdminRoute = ({ children }) => {
  const { token, isAdmin, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center h-screen text-gray-500">Loading...</div>;
  if (!token) return <Navigate to="/login" replace />;
  if (!isAdmin) return <Navigate to="/dashboard" replace />;
  return children;
};
 