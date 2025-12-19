import { createContext, useContext, useState } from "react";

const AuthContext = createContext();


function getStoredUser() {
  try {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  } catch (err) {
    console.error("Invalid user in localStorage", err);
    localStorage.removeItem("user");
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => getStoredUser());

  const login = (data) => {
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    localStorage.setItem("user", JSON.stringify(data.user));
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
