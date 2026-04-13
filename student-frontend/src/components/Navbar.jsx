import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import toast from "react-hot-toast";
 
const Navbar = () => {
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
 
  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
    navigate("/login");
  };
 
  return (
    <nav className="bg-indigo-600 text-white px-6 py-3 flex items-center justify-between shadow-md">
      <div className="flex items-center gap-6">
        <Link to="/dashboard" className="font-bold text-lg tracking-tight">
          Student API
        </Link>
        <Link to="/dashboard" className="text-sm hover:text-indigo-200 transition">
          Dashboard
        </Link>
        {isAdmin && (
          <Link to="/students/create" className="text-sm hover:text-indigo-200 transition">
            Add Student
          </Link>
        )}
      </div>
 
      <div className="flex items-center gap-4">
        <span className="text-sm text-indigo-200">
          {user?.username}
          <span className="ml-2 bg-indigo-800 text-indigo-100 text-xs px-2 py-0.5 rounded-full">
            {user?.role}
          </span>
        </span>
        <button
          onClick={handleLogout}
          className="text-sm bg-indigo-800 hover:bg-indigo-900 px-3 py-1.5 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};
 
export default Navbar;