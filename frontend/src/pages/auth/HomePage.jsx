import { 
  Button, 
  Container, 
  Typography,
  Stack,
  Box,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function Login() {

  const navigate = useNavigate();

  const handleLogin = (e) => {
    
    e.preventDefault();
    navigate("/login");

  };

  const handleRegister = (e) => {
    
    e.preventDefault();
    navigate("/register");

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
          <Button onClick={handleLogin}>Login</Button>
          <Button onClick={handleRegister}>Register</Button>
        </Stack>
      </Container>
    </Box>

  );

}
