
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import StudentDashboard from "./pages/student/StudentDashboard";
import MentorDashboard from "./pages/mentor/MentorDashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";
import RoleGuard from "./auth/RoleGuard";
import HomePage from "./pages/auth/HomePage";
import { Fragment } from "react";
import Navbar from "./components/Navbar";
import UserManagement from "./pages/admin/UserManagement";

export default function App() {
  return (<Fragment>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/student" element={
          <RoleGuard role="Student">
            <StudentDashboard />
          </RoleGuard>
        } />

        <Route path="/mentor" element={
          <RoleGuard role="Mentor">
            <MentorDashboard />
          </RoleGuard>
        } />

        <Route path="/admin" element={
          <RoleGuard role="Admin">
            <AdminDashboard />
          </RoleGuard>
        } />

        <Route path="/user-management" element={
          <RoleGuard role="Admin">
            <UserManagement />
          </RoleGuard>
        } />

      </Routes>

    </Fragment>);
}
