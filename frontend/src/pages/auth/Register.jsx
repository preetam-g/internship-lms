
import { Button, TextField, Container, Typography } from "@mui/material";
import axios from "axios";

export default function Register() {
  const submit = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    await axios.post("http://localhost:8000/api/auth/register", {
      email: data.get("email"),
      password: data.get("password"),
    });
    window.location.href = "/login";
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>Register</Typography>
      <form onSubmit={submit}>
        <TextField fullWidth label="Email" name="email" margin="normal" />
        <TextField fullWidth label="Password" name="password" type="password" margin="normal" />
        <Button fullWidth variant="contained" type="submit">Register</Button>
      </form>
    </Container>
  );
}
