import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import API from "../api/axios";
 
export const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("verifying");
 
  useEffect(() => {
    const token = searchParams.get("token");
    if (!token) { setStatus("invalid"); return; }
    API.get(`/api/v1/auth/verify-email?token=${token}`)
      .then(() => setStatus("success"))
      .catch(() => setStatus("error"));
  }, []);
 
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-sm border border-gray-200 p-8 text-center">
        {status === "verifying" && <p className="text-gray-500">Verifying your email...</p>}
        {status === "success" && (
          <>
            <div className="text-5xl mb-4">✅</div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Email verified!</h2>
            <p className="text-sm text-gray-500 mb-6">Your account is now active. You can log in.</p>
            <Link to="/login" className="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-indigo-700 transition">Go to Login</Link>
          </>
        )}
        {(status === "error" || status === "invalid") && (
          <>
            <div className="text-5xl mb-4">❌</div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Verification failed</h2>
            <p className="text-sm text-gray-500 mb-6">The link is invalid or has expired.</p>
            <Link to="/login" className="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-indigo-700 transition">Back to Login</Link>
          </>
        )}
      </div>
    </div>
  );
};
 
export const ForgotPassword = () => {
  const [email, setEmail]     = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent]       = useState(false);
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await API.post("/api/v1/auth/forgot-password", { email });
      setSent(true);
    } catch {
      setSent(true); // Always show success to prevent enumeration
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">Forgot password</h1>
        <p className="text-sm text-gray-500 mb-6">Enter your email and we'll send you a reset link.</p>
 
        {sent ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-sm text-green-700">
            If that email is registered, a reset link has been sent. Check your inbox.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="you@gmail.com"
              />
            </div>
            <button
              type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg transition text-sm disabled:opacity-60"
            >
              {loading ? "Sending..." : "Send reset link"}
            </button>
          </form>
        )}
 
        <p className="text-center text-sm text-gray-500 mt-6">
          <Link to="/login" className="text-indigo-600 hover:underline">Back to login</Link>
        </p>
      </div>
    </div>
  );
};
 
export const ResetPassword = () => {
  const [searchParams]        = useSearchParams();
  const [form, setForm]       = useState({ new_password: "", confirm: "" });
  const [loading, setLoading] = useState(false);
  const [done, setDone]       = useState(false);
  const [error, setError]     = useState("");
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.new_password !== form.confirm) { setError("Passwords do not match"); return; }
    setLoading(true);
    setError("");
    try {
      await API.post("/api/v1/auth/reset-password", {
        token: searchParams.get("token"),
        new_password: form.new_password
      });
      setDone(true);
    } catch (err) {
      setError(err.response?.data?.detail || "Reset failed. Link may have expired.");
    } finally {
      setLoading(false);
    }
  };
 
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-sm border border-gray-200 p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">Reset password</h1>
        <p className="text-sm text-gray-500 mb-6">Enter your new password below.</p>
 
        {done ? (
          <div className="text-center">
            <div className="text-5xl mb-4">✅</div>
            <p className="text-sm text-gray-600 mb-6">Password reset successfully!</p>
            <Link to="/login" className="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm hover:bg-indigo-700 transition">Go to Login</Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-lg px-3 py-2">{error}</div>}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">New password</label>
              <input
                type="password" value={form.new_password}
                onChange={(e) => setForm({ ...form, new_password: e.target.value })} required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="••••••••"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm password</label>
              <input
                type="password" value={form.confirm}
                onChange={(e) => setForm({ ...form, confirm: e.target.value })} required
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="••••••••"
              />
            </div>
            <button
              type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 rounded-lg transition text-sm disabled:opacity-60"
            >
              {loading ? "Resetting..." : "Reset password"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
