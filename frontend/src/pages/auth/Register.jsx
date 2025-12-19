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
import { registerUser } from "../../api/apiFunctions"; 
import { useNavigate } from "react-router-dom";

export default function Register() {

  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submit = (e) => {
    e.preventDefault();

    if (!username || !password || !firstName || !lastName || !email) {
      setError("All fields are required");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    const dta = {
      username,
      password,
      first_name: firstName,
      last_name: lastName,
      email,
    };

    setLoading(true);
    setError(null);

    registerUser(dta)
      .then(res => {
        const dta = res.data.data;
        login(dta);

        let nxt = "";
        switch (dta.user.role_name) {
          case "Admin": nxt = "/admin"; break;
          case "Mentor": nxt = "/mentor"; break;
          default: nxt = "/student";
        }

        navigate(nxt);
      })
      .catch(err => {
        console.error(err);
        const msg =
          err?.response?.data?.detail ||
          "Registration failed. Please try again.";
        setError(msg);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Box sx={{ height: "95vh", alignContent: "center" }}>
      <Container
        maxWidth="sm"
        sx={{ display: "flex", justifyContent: "center" }}
      >
        <Stack spacing={2} sx={{ width: "80%", minWidth: 200 }}>
          <Typography variant="h4" gutterBottom>
            Register
          </Typography>

          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            fullWidth
            size="small"
            label="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
          />

          <TextField
            fullWidth
            size="small"
            label="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />

          <TextField
            fullWidth
            size="small"
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <TextField
            fullWidth
            size="small"
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <TextField
            fullWidth
            size="small"
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            disabled={loading}
            variant="contained"
            onClick={submit}
          >
            {loading ? "Registering..." : "Register"}
          </Button>

          <Stack
            direction={{ xs: "column", sm: "row" }}
            sx={{
              display: "flex",
              justifyContent: "space-evenly",
              alignItems: "center",
              mt: 1,
            }}
          >
            <Typography variant="body2">
              Already have an account?
            </Typography>
            <Button onClick={() => navigate("/login")}>
              Login
            </Button>
          </Stack>
        </Stack>
      </Container>
    </Box>
  );
}
