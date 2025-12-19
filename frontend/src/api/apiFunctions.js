// src/api/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

/* ---------------------------
   Request Interceptor
---------------------------- */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* ---------------------------
   Response Interceptor
   -> Logout on 401
---------------------------- */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      // 🔥 Clear ALL auth data
      localStorage.clear();

      // Prevent redirect loop on login/register
      const currentPath = window.location.pathname;
      if (
        currentPath !== "/login" &&
        currentPath !== "/register"
      ) {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

/* ===========================
   API FUNCTIONS
=========================== */

// authentication
export const registerUser = (data) => {
  return api.post("auth/register/", data);
};

export const loginUser = (data) => {
  return api.post("auth/login/", data);
};

// user-management
export const getUsers = (params) => {
  return api.get("users/", { params });
};

export const approveMentor = (id, data) => {
  return api.put(`users/${id}/approve-mentor/`, data);
};

export const deleteUser = (id) => {
  return api.delete(`users/${id}/`);
};

// courses
export const getCourses = (params) => {
  // for admin to get all courses
  return api.get("courses/", {params});
};