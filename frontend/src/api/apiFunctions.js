// src/api/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});


// authentication
export const registerUser = (data) => {
  return api.post("auth/register/", data);
};

export const loginUser = (data) => {
  return api.post("auth/login/", data);
};

// user-management
export const getUsers = (params) => {
  return api.get("users/", {params});
};

export const approveMentor = (id, data) => {
  return api.put(`users/${id}/approve-mentor/`, data);
};

export const deleteUser = (id) => {
  return api.delete(`users/${id}/`);
};