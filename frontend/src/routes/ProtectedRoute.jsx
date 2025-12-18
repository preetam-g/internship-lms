
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ role, children }) {
  const storedRole = localStorage.getItem("role");
  if (!storedRole) return <Navigate to="/login" />;
  if (role && role !== storedRole) return <Navigate to="/login" />;
  return children;
}
