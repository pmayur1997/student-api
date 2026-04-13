import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";
import toast from "react-hot-toast";
 
const Dashboard = () => {
  const { isAdmin } = useAuth();
  const [students, setStudents]   = useState([]);
  const [loading, setLoading]     = useState(true);
  const [page, setPage]           = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal]         = useState(0);
 
  const [filters, setFilters] = useState({
    search: "", course: "", grade: "",
    min_age: "", max_age: "", sort_by: "name", order: "asc"
  });
 
  const fetchStudents = async () => {
    setLoading(true);
    try {
      const params = { page, per_page: 10, ...filters };
      Object.keys(params).forEach((k) => !params[k] && delete params[k]);
      const res = await API.get("/api/v1/students", { params });
      setStudents(res.data.data.data);
      setTotalPages(res.data.data.total_pages);
      setTotal(res.data.data.total);
    } catch (err) {
      toast.error("Failed to fetch students");
    } finally {
      setLoading(false);
    }
  };
 
  useEffect(() => { fetchStudents(); }, [page, filters]);
 
  const handleDelete = async (id) => {
    if (!window.confirm("Delete this student?")) return;
    try {
      await API.delete(`/api/v1/students/${id}`);
      toast.success("Student deleted");
      fetchStudents();
    } catch {
      toast.error("Delete failed");
    }
  };
 
  const handleExport = (format) => {
    const token = localStorage.getItem("token");
    /*window.open(
      `https://student-api-production-5b6d.up.railway.app/api/v1/export/students?format=${format}&token=${token}`,
      "_blank"
    );*/
    // Use axios for proper auth header
    API.get(`/api/v1/export/students?format=${format}`, { responseType: "blob" })
      .then((res) => {
        const ext = format === "excel" ? "xlsx" : format;
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const a   = document.createElement("a");
        a.href    = url;
        a.download = `students_export.${ext}`;
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch(() => toast.error("Export failed"));
  };
 
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
 
      <div className="max-w-7xl mx-auto px-4 py-8">
 
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Students</h1>
            <p className="text-sm text-gray-500">{total} total records</p>
          </div>
          <div className="flex gap-2">
            {/* Export buttons */}
            <button onClick={() => handleExport("csv")}
              className="text-xs border border-gray-300 hover:bg-gray-100 px-3 py-1.5 rounded-lg transition">
              Export CSV
            </button>
            <button onClick={() => handleExport("excel")}
              className="text-xs border border-gray-300 hover:bg-gray-100 px-3 py-1.5 rounded-lg transition">
              Export Excel
            </button>
            {/* Add Student button for admins */}
            {/*
            {isAdmin && (
              <Link to="/students/create"
                className="text-xs bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1.5 rounded-lg transition">
                + Add Student
              </Link>
            )}
          */}
          </div>
        </div>
 
        {/* Filters */}
        <div className="bg-white border border-gray-200 rounded-xl p-4 mb-6 grid grid-cols-2 md:grid-cols-4 gap-3">
          <input placeholder="Search name or email" value={filters.search}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 col-span-2 md:col-span-1" />
          <input placeholder="Course" value={filters.course}
            onChange={(e) => setFilters({ ...filters, course: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <input placeholder="Grade" value={filters.grade}
            onChange={(e) => setFilters({ ...filters, grade: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          <select value={filters.sort_by}
            onChange={(e) => setFilters({ ...filters, sort_by: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="name">Sort: Name</option>
            <option value="age">Sort: Age</option>
            <option value="course">Sort: Course</option>
            <option value="grade">Sort: Grade</option>
          </select>
          <select value={filters.order}
            onChange={(e) => setFilters({ ...filters, order: e.target.value })}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
          <button onClick={() => { setFilters({ search: "", course: "", grade: "", min_age: "", max_age: "", sort_by: "name", order: "asc" }); setPage(1); }}
            className="text-sm text-gray-500 hover:text-gray-700 underline">
            Clear filters
          </button>
        </div>
 
        {/* Table */}
        <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
          {loading ? (
            <div className="text-center py-16 text-gray-400 text-sm">Loading students...</div>
          ) : students.length === 0 ? (
            <div className="text-center py-16 text-gray-400 text-sm">No students found</div>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  {["Name", "Email", "Age", "Course", "Grade", ...(isAdmin ? ["Actions"] : [])].map((h) => (
                    <th key={h} className="text-left px-4 py-3 font-medium text-gray-600 text-xs uppercase tracking-wide">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {students.map((s) => (
                  <tr key={s.id} className="hover:bg-gray-50 transition">
                    <td className="px-4 py-3 font-medium text-gray-800">{s.name}</td>
                    <td className="px-4 py-3 text-gray-500">{s.email}</td>
                    <td className="px-4 py-3 text-gray-500">{s.age}</td>
                    <td className="px-4 py-3">
                      <span className="bg-indigo-50 text-indigo-700 text-xs px-2 py-1 rounded-full">{s.course}</span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="bg-green-50 text-green-700 text-xs px-2 py-1 rounded-full">{s.grade || "N/A"}</span>
                    </td>
                    {isAdmin && (
                      <td className="px-4 py-3 flex gap-2">
                        <Link to={`/students/edit/${s.id}`}
                          className="text-xs bg-amber-50 text-amber-700 border border-amber-200 px-2 py-1 rounded hover:bg-amber-100 transition">
                          Edit
                        </Link>
                        <button onClick={() => handleDelete(s.id)}
                          className="text-xs bg-red-50 text-red-600 border border-red-200 px-2 py-1 rounded hover:bg-red-100 transition">
                          Delete
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
 
        {/* Pagination */}
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-gray-500">Page {page} of {totalPages}</p>
          <div className="flex gap-2">
            <button disabled={page === 1} onClick={() => setPage(page - 1)}
              className="text-sm px-3 py-1.5 border border-gray-300 rounded-lg disabled:opacity-40 hover:bg-gray-100 transition">
              Previous
            </button>
            <button disabled={page === totalPages} onClick={() => setPage(page + 1)}
              className="text-sm px-3 py-1.5 border border-gray-300 rounded-lg disabled:opacity-40 hover:bg-gray-100 transition">
              Next
            </button>
          </div>
        </div>
 
      </div>
    </div>
  );
};
 
export default Dashboard;