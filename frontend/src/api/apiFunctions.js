// src/api/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});


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
  return api.get("courses/", {params});
};

export const getMyCourses = (params) => {
  return api.get("courses/my/", {params});
};

export const createCourse = (data) => {
  return api.post("courses/", data);
};

export const updateCourse = (id, data) => {
  return api.put(`courses/${id}/`, data);
};

export const deleteCourse = (id) => {
  return api.delete(`courses/${id}/`);
};

export const addChapter = (courseId, data) => {
  return api.post(`courses/${courseId}/chapters/`, data);
};

export const assignCourse = (courseId, data) => {
  return api.post(`courses/${courseId}/assign/`, data);
};

export const getAllStudents = (params) => {
  return api.get("users/students/", {params});
};

export const getEnrolledCourses = () =>
  api.get("courses/enrolled/");

export const getCourseChapters = (courseId) =>
  api.get(`courses/${courseId}/chapters/`);

export const markChapterComplete = (chapterId) =>
  api.post(`progress/${chapterId}/complete/`);

export const getMyProgress = () =>
  api.get("progress/my/");

export const downloadCertificate = (courseId) =>
  api.get(`certificates/${courseId}/`, {
    responseType: "blob",
  });