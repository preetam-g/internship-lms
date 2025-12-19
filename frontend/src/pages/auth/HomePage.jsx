import { 
  Button, 
  Container, 
  Typography,
  Stack,
  Box,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { Fragment } from "react";

export default function Login() {

  const navigate = useNavigate();
  const {user} = useAuth();

  const handleLogin = (e) => {
    
    e.preventDefault();
    navigate("/login");

  };

  const handleRegister = (e) => {
    
    e.preventDefault();
    navigate("/register");

  };

  const handleDashboard = (e) => {
    
    e.preventDefault();
    if (!user) return;
    navigate(`/${user?.role_name.toLowerCase()}`);

  };

  return (
    <Box
      sx={{
        height: "95vh",
        alignContent: "center"
      }}
    >
      <Container 
        maxWidth="sm"
        sx={{
          display: "flex",
          justifyContent: "center"
        }}
      >
        <Stack>
            <Typography variant="h4" gutterBottom>Internship Page</Typography>
        {!user ? (
          <Fragment>
            <Button onClick={handleLogin} size="small">Login</Button>
            <Button onClick={handleRegister} size="small">Register</Button>
          </Fragment>
        ) : (
          <Fragment>
            <Button onClick={handleDashboard} size="small">Go to Dashboard</Button>
          </Fragment>
        )}
        </Stack>
      </Container>
    </Box>

  );

}
