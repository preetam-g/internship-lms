import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <AppBar position="sticky">
      <Toolbar>
        {/* Left side */}
        <Typography
          variant="h6"
          sx={{ flexGrow: 1, cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          LMS
        </Typography>

        {/* Right side */}
        {user ? (
          <Box>
            <Typography
              variant="body2"
              sx={{ mr: 2, display: "inline" }}
              onClick={e => navigate(user.role_name.toLowerCase())}
            >
              {user.role_name.toUpperCase()}
            </Typography>

            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          </Box>
        ) : (
          <>
            <Button color="inherit" onClick={() => navigate("/login")}>
              Login
            </Button>
            <Button color="inherit" onClick={() => navigate("/register")}>
              Register
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}
