import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import toast from "react-hot-toast";
 
const StudentForm = ({ isEdit }) => {
  const navigate        = useNavigate();
  const { id }          = useParams();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: "", email: "", age: "", course: "", grade: ""
  });
 
  useEffect(() => {
    if (isEdit && id) {
      API.get(`/api/v1/students/${id}`)
        .then((res) => {
          const s = res.data.data;
          setForm({ name: s.name, email: s.email, age: s.age, course: s.course, grade: s.grade || "" });
        })
        .catch(() => toast.error("Failed to load student"));
    }
  }, [id]);
 
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...form, age: parseInt(form.age) };
      if (isEdit) {
        await API.put(`/api/v1/students/${id}`, payload);
        toast.success("Student updated!");
      } else {
        await API.post("/api/v1/students", payload);
        toast.success("Student created!");
      }
      navigate("/dashboard");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-xl mx-auto px-4 py-10">
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-1">
            {isEdit ? "Edit Student" : "Add Student"}
          </h1>
          <p className="text-sm text-gray-500 mb-6">
            {isEdit ? "Update student details below." : "Fill in the details to add a new student."}
          </p>
 
          <form onSubmit={handleSubmit} className="space-y-4">
            {[
              { label: "Full name",  name: "name",   type: "text",   placeholder: "John Doe" },
              { label: "Email",      name: "email",  type: "email",  placeholder: "john@gmail.com" },
              { label: "Age",        name: "age",    type: "number", placeholder: "20" },
              { label: "Course",     name: "course", type: "text",   placeholder: "Computer Science" },
              { label: "Grade",      name: "grade",  type: "text",   placeholder: "A" },
            ].map((field) => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{field.label}</label>
                <input
                  type={field.type} name={field.name}
                  value={form[field.name]} onChange={handleChange}
                  placeholder={field.placeholder}
                  required={field.name !== "grade"}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            ))}
 
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={() => navigate("/dashboard")}
                className="flex-1 border border-gray-300 text-gray-600 hover:bg-gray-50 font-medium py-2 rounded-lg transition text-sm">
                Cancel
              </button>
              <button type="submit" disabled={loading}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg transition text-sm disabled:opacity-60">
                {loading ? "Saving..." : isEdit ? "Update Student" : "Add Student"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
 
export const CreateStudent = () => <StudentForm isEdit={false} />;
export const EditStudent   = () => <StudentForm isEdit={true} />;