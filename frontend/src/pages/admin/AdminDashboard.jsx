import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Stack,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import PeopleIcon from "@mui/icons-material/People";
import SchoolIcon from "@mui/icons-material/School";
import BarChartIcon from "@mui/icons-material/BarChart";
import { useEffect, useState } from "react";

import {
  getUsers,
  getCourses,
} from "../../api/apiFunctions";

import UserManagement from "./UserManagement";



export default function AdminDashboard() {

  const [users, setUsers] = useState([]);
  const [courses, setCourses] = useState([]);

  const [loadingUsers, setLoadingUsers] = useState(false);
  const [loadingCourses, setLoadingCourses] =
    useState(false);

  const [openUsersDialog, setOpenUsersDialog] =
    useState(false);
  const [openCoursesDialog, setOpenCoursesDialog] =
    useState(false);


  useEffect(() => {
    fetchUsers();
    fetchCourses();
  }, []);

  /* ---------------------------
     API Calls
  ---------------------------- */
  const fetchUsers = () => {
    setLoadingUsers(true);
    getUsers()
      .then((res) => {
        setUsers(res.data.data || []);
      })
      .catch((err) => {
        alert(
          err?.response?.data?.detail ||
            "Error fetching users"
        );
      })
      .finally(() => setLoadingUsers(false));
  };

  const fetchCourses = () => {
    setLoadingCourses(true);
    getCourses()
      .then((res) => {
        setCourses(res.data.data || []);
      })
      .catch((err) => {
        alert(
          err?.response?.data?.detail ||
            "Error fetching courses"
        );
      })
      .finally(() => setLoadingCourses(false));
  };

  /* ---------------------------
     Dialogs
  ---------------------------- */

  const UserManagementDialog = () => (
    <Dialog
      open={openUsersDialog}
      onClose={() => setOpenUsersDialog(false)}
      fullWidth
      maxWidth="lg"
    >
      <DialogTitle
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        User Management
        <IconButton
          onClick={() => setOpenUsersDialog(false)}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        <UserManagement
          users={users}
          loading={loadingUsers}
          refreshUsers={fetchUsers}
        />
      </DialogContent>
    </Dialog>
  );

  const CourseManagementDialog = () => (
    <Dialog
      open={openCoursesDialog}
      onClose={() => setOpenCoursesDialog(false)}
      fullWidth
      maxWidth="lg"
    >
      <DialogTitle
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        All Courses
        <IconButton
          onClick={() => setOpenCoursesDialog(false)}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        {loadingCourses ? (
          <Typography>Loading courses...</Typography>
        ) : courses.length === 0 ? (
          <Typography>No courses found.</Typography>
        ) : (
          <Grid container spacing={3}>
            {courses.map((course) => (
              <Grid
                item
                xs={12}
                md={6}
                key={course.id}
              >
                <Card>
                  <CardContent>
                    <Typography variant="h6">
                      {course.title}
                    </Typography>

                    <Typography
                      variant="body2"
                      color="text.secondary"
                      mb={1}
                    >
                      {course.description ||
                        "No description"}
                    </Typography>

                    {/* <Typography variant="caption">
                      Mentor:{" "}
                      {course.mentor?.username ||
                        "—"}
                    </Typography> */}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </DialogContent>
    </Dialog>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 1 }}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      {/* Stats */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Total Users"
            value={users.length}
            icon={<PeopleIcon />}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard
            title="Total Courses"
            value={courses.length}
            icon={<SchoolIcon />}
          />
        </Grid>

        {/* <Grid item xs={12} md={3}>
          <StatCard
            title="Completions"
            value="--"
            icon={<BarChartIcon />}
          />
        </Grid> */}
      </Grid>

      <Divider sx={{ my: 4 }} />

      {/* Actions */}
      <Typography variant="h5" gutterBottom>
        Administrative Actions
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <ActionCard
            title="User Management"
            description="View and manage all users on the platform."
            actionLabel="Manage Users"
            onClick={() =>
              setOpenUsersDialog(true)
            }
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <ActionCard
            title="Course Management"
            description="View all courses on the platform."
            actionLabel="View Courses"
            onClick={() => {
              setOpenCoursesDialog(true);
            }}
          />
        </Grid>
      </Grid>

      {/* Dialogs */}
      <UserManagementDialog />
      <CourseManagementDialog />
    </Container>
  );
}

/* ===========================
   Helper Components
=========================== */

function StatCard({ title, value, icon }) {
  return (
    <Card>
      <CardContent>
        <Stack
          direction="row"
          spacing={2}
          alignItems="center"
        >
          {icon}
          <div>
            <Typography
              variant="subtitle2"
              color="text.secondary"
            >
              {title}
            </Typography>
            <Typography variant="h5">
              {value}
            </Typography>
          </div>
        </Stack>
      </CardContent>
    </Card>
  );
}

function ActionCard({
  title,
  description,
  actionLabel,
  onClick,
}) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          mb={2}
        >
          {description}
        </Typography>

        <Button variant="contained" onClick={onClick}>
          {actionLabel}
        </Button>
      </CardContent>
    </Card>
  );
}
