import { 
  TextField, 
  Container, 
  Typography, 
  Box, 
  Stack, 
  Alert,
  Button
} from "@mui/material";
import { useAuth } from "../../auth/AuthContext";
import { useState } from "react";
import { loginUser } from "../../api/apiFunctions"; 
import { useNavigate } from "react-router-dom";

export default function Login() {

  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = (e) => {

    e.preventDefault();
    const dta = { username, password };

    if (!username || !password)
    {
      setError("Username and Password cannot be empty");
      return;
    }

    setLoading(true);
    setError(null);

    loginUser(dta)
      .then(res => {
        
        const dta = res.data.data;
        login(dta);

        let nxt = "";
        switch (dta.user.role_name)
        {
          case 'Admin': nxt = "/admin"; break;
          case 'Mentor': nxt = "/mentor"; break;
          default: nxt = "/student"; 
        }
        navigate(nxt);

      })
      .catch(err => {
        console.error(err);
        const msg = "Login failed. Please try again.";
        setError(msg);
      })
      .finally(() => {
        setLoading(false);
      });
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
        <Stack spacing={2} 
          sx={{
            width: "80%",
            minWidth: 200,
          }}
        >
          <Typography variant="h4" gutterBottom>Login</Typography>
          
          {error && <Alert severity="error">{error}</Alert>}

          <TextField 
            fullWidth
            size="small"
            type="text"
            label="Username" 
            name="username"
            value={username}
            onChange={e => setUsername(e.target.value)}
          />

          <TextField 
            fullWidth
            size="small"
            type="password"
            label="Password"
            name="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />

          <Button 
            disabled={loading}
            variant="contained" 
            onClick={submit}
          >
            Verify
          </Button>

          <Stack direction={{xs: "column", sm: "row"}}
            sx={{
              display: "flex",
              justifyContent: 'space-evenly',
              alignItems: "center",
              mt: 1
            }}
          >
            <Typography variant="body2">Don't have an account?</Typography>
            <Button onClick={() => navigate("/register")}>Register</Button>
          </Stack>

        </Stack>
      </Container>
    </Box>
  );
}