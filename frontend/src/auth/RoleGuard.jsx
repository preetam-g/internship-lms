
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function RoleGuard({ role, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (user.role_name !== role) return <Navigate to="/login" />;
  return children;
}
