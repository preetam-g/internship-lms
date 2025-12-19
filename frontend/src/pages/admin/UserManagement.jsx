import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Stack,
  TextField,
  MenuItem,
} from "@mui/material";
import { useState } from "react";
import { approveMentor } from "../../api/apiFunctions";

export default function UserManagement({
  users,
  refreshUsers,
  loading,
}) {
  const [roleFilter, setRoleFilter] = useState("ALL");
  const [actionLoading, setActionLoading] = useState(null);

  /* ---------------------------
     Role Counts (global)
  ---------------------------- */
  const counts = users.reduce(
    (acc, user) => {
      acc.total += 1;
      acc[user.role_name] =
        (acc[user.role_name] || 0) + 1;
      return acc;
    },
    {
      total: 0,
      Admin: 0,
      Mentor: 0,
      Student: 0,
    }
  );

  /* ---------------------------
     Filtered Users
  ---------------------------- */
  const filteredUsers = users.filter(
    (user) =>
      roleFilter === "ALL" ||
      user.role_name === roleFilter
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 1 }}>
      <Typography variant="h4" gutterBottom>
        User Management
      </Typography>

      {/* Role Counts */}
      <Stack
        direction="row"
        spacing={1.5}
        sx={{ mb: 3 }}
        flexWrap="wrap"
      >
        <Chip
          label={`Total: ${counts.total}`}
          color="primary"
          variant="outlined"
        />
        <Chip
          label={`Admins: ${counts.Admin}`}
          color="error"
          variant="outlined"
        />
        <Chip
          label={`Mentors: ${counts.Mentor}`}
          color="success"
          variant="outlined"
        />
        <Chip
          label={`Students: ${counts.Student}`}
          color="secondary"
          variant="outlined"
        />
      </Stack>

      {/* Filters */}
      <Stack
        direction={{ xs: "column", md: "row" }}
        spacing={2}
        sx={{ mb: 3 }}
      >
        <TextField
          select
          label="Filter by role"
          value={roleFilter}
          onChange={(e) =>
            setRoleFilter(e.target.value)
          }
          sx={{ minWidth: 200 }}
        >
          <MenuItem value="ALL">All</MenuItem>
          <MenuItem value="Admin">Admin</MenuItem>
          <MenuItem value="Mentor">Mentor</MenuItem>
          <MenuItem value="Student">Student</MenuItem>
        </TextField>
      </Stack>

      {loading && (
        <Typography sx={{ mb: 2 }}>
          Loading users...
        </Typography>
      )}

      <Grid container spacing={3}>
        {filteredUsers.map((user) => (
          <Grid
            item
            xs={12}
            sm={6}
            md={4}
            key={user.id}
          >
            <UserCard
              user={user}
              refreshUsers={refreshUsers}
              actionLoading={actionLoading}
              setActionLoading={setActionLoading}
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

/* ===========================
   User Card
=========================== */

function UserCard({
  user,
  refreshUsers,
  actionLoading,
  setActionLoading,
}) {
  const isStudent =
    user.role_name === "Student";

  const COLORS = {
    Admin: "error",
    Mentor: "success",
    Student: "secondary",
  };

  const makeMentor = async () => {
    try {
      setActionLoading(user.id);
      await approveMentor(user.id);
      refreshUsers();
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        "Failed to approve mentor";
      alert(msg);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <Card sx={{ height: "100%" }}>
      <CardContent
        sx={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          mb={1}
        >
          <Chip
            label={user.role_name}
            color={COLORS[user.role_name]}
            size="small"
          />

          <Button
            size="small"
            variant="contained"
            disabled={
              !isStudent ||
              actionLoading === user.id
            }
            onClick={makeMentor}
          >
            {actionLoading === user.id
              ? "Processing..."
              : "Make Mentor"}
          </Button>
        </Stack>

        {/* User Info */}
        <Stack spacing={0.8}>
          <Typography variant="body2">
            <b>Username:</b>{" "}
            {user.username}
          </Typography>

          <Typography variant="body2">
            <b>Email:</b> {user.email}
          </Typography>

          <Typography variant="body2">
            <b>First Name:</b>{" "}
            {user.first_name}
          </Typography>

          <Typography variant="body2">
            <b>Last Name:</b>{" "}
            {user.last_name}
          </Typography>
        </Stack>

        <div style={{ flexGrow: 1 }} />
      </CardContent>
    </Card>
  );
}
