
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import StudentDashboard from "./pages/student/StudentDashboard";
import MentorDashboard from "./pages/mentor/MentorDashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";
import RoleGuard from "./auth/RoleGuard";
import HomePage from "./pages/auth/HomePage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/student" element={
        <RoleGuard role="student">
          <StudentDashboard />
        </RoleGuard>
      } />

      <Route path="/mentor" element={
        <RoleGuard role="mentor">
          <MentorDashboard />
        </RoleGuard>
      } />

      <Route path="/admin" element={
        <RoleGuard role="admin">
          <AdminDashboard />
        </RoleGuard>
      } />
    </Routes>
  );
}
