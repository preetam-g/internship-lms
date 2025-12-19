
import { Button, TextField, Container, Typography } from "@mui/material";
import axios from "axios";
import { useAuth } from "../../auth/AuthContext";

export default function Login() {
  const { login } = useAuth();

  const submit = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    const res = await axios.post("http://localhost:8000/api/auth/login", {
      email: data.get("email"),
      password: data.get("password"),
    });
    login(res.data);
    window.location.href = "/" + res.data.user.role;
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>Login</Typography>
      <form onSubmit={submit}>
        <TextField fullWidth label="Email" name="email" margin="normal" />
        <TextField fullWidth label="Password" name="password" type="password" margin="normal" />
        <Button fullWidth variant="contained" type="submit">Login</Button>
      </form>
    </Container>
  );
}
