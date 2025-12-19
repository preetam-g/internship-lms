import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Divider,
  IconButton,
  MenuItem,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";
import PersonAddIcon from "@mui/icons-material/PersonAdd";

import { useEffect, useState } from "react";

import {
  getMyCourses,
  createCourse,
  updateCourse,
  deleteCourse,
  addChapter,
  getAllStudents,
  assignCourse,
} from "../../api/apiFunctions";

export default function MentorDashboard() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);

  /* Loading states */
  const [creatingCourse, setCreatingCourse] = useState(false);
  const [updatingCourse, setUpdatingCourse] = useState(false);
  const [addingChapter, setAddingChapter] = useState(false);
  const [assigningCourse, setAssigningCourse] = useState(false);
  const [fetchingStudents, setFetchingStudents] = useState(false);

  /* Dialog states */
  const [openCreateCourse, setOpenCreateCourse] = useState(false);
  const [openEditCourse, setOpenEditCourse] = useState(false);
  const [openAddChapter, setOpenAddChapter] = useState(false);
  const [openViewChapter, setOpenViewChapter] = useState(false);
  const [openAssign, setOpenAssign] = useState(false);

  /* Course state */
  const [editingCourse, setEditingCourse] = useState(null);
  const [courseTitle, setCourseTitle] = useState("");
  const [courseDescription, setCourseDescription] = useState("");

  /* Chapter state */
  const [activeCourse, setActiveCourse] = useState(null);
  const [chapterData, setChapterData] = useState({
    title: "",
    description: "",
    video_url: "",
    image_url: "",
  });
  const [viewChapter, setViewChapter] = useState(null);

  /* Assign state */
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState("");

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  useEffect(() => {
    fetchMyCourses();
  }, []);

  const fetchMyCourses = () => {
    setLoading(true);
    getMyCourses()
      .then((res) => setCourses(res.data.data || []))
      .catch(() => alert("Failed to load courses"))
      .finally(() => setLoading(false));
  };

  const fetchStudents = () => {
    setFetchingStudents(true);
    getAllStudents()
      .then((res) => setStudents(res.data.data || []))
      .catch(() => alert("Failed to fetch students"))
      .finally(() => setFetchingStudents(false));
  };

  /* Course CRUD */
  const handleCreateCourse = () => {
    if (!courseTitle) return alert("Title is required");

    setCreatingCourse(true);
    createCourse({ title: courseTitle, description: courseDescription })
      .then(() => {
        setOpenCreateCourse(false);
        setCourseTitle("");
        setCourseDescription("");
        fetchMyCourses();
      })
      .catch(() => alert("Failed to create course"))
      .finally(() => setCreatingCourse(false));
  };

  const handleUpdateCourse = () => {
    setUpdatingCourse(true);
    updateCourse(editingCourse.id, {
      title: courseTitle,
      description: courseDescription,
    })
      .then(() => {
        setOpenEditCourse(false);
        setEditingCourse(null);
        fetchMyCourses();
      })
      .catch(() => alert("Failed to update course"))
      .finally(() => setUpdatingCourse(false));
  };

  const handleDeleteCourse = (courseId) => {
    if (!window.confirm("Delete this course permanently?")) return;

    deleteCourse(courseId)
      .then(fetchMyCourses)
      .catch(() => alert("Failed to delete course"));
  };

  /* Chapters */
  const openAddChapterDialog = (course) => {
    setActiveCourse(course);
    setChapterData({
      title: "",
      description: "",
      video_url: "",
      image_url: "",
    });
    setOpenAddChapter(true);
  };

  const handleAddChapter = () => {
    if (!chapterData.title) return alert("Chapter title required");
    if (!chapterData.video_url) return alert("Video URL required");
    if (!isValidUrl(chapterData.video_url)) return alert("Invalid video URL");
    if (chapterData.image_url && !isValidUrl(chapterData.image_url))
      return alert("Invalid image URL");

    const nextSeq =
      activeCourse.chapters?.length > 0
        ? Math.max(...activeCourse.chapters.map((c) => c.sequence_number)) + 1
        : 1;

    setAddingChapter(true);
    addChapter(activeCourse.id, {
      ...chapterData,
      sequence_number: nextSeq,
    })
      .then(() => {
        setOpenAddChapter(false);
        setActiveCourse(null);
        fetchMyCourses();
      })
      .catch(() => alert("Failed to add chapter"))
      .finally(() => setAddingChapter(false));
  };

  /* Assign Course */
  const handleAssignCourse = () => {
    if (!selectedStudent) return alert("Select a student");

    setAssigningCourse(true);
    assignCourse(activeCourse.id, {
      student_id: selectedStudent,
    })
      .then(() => {
        alert("Course assigned successfully");
        setOpenAssign(false);
        setActiveCourse(null);
      })
      .catch(() => alert("Failed to assign course"))
      .finally(() => setAssigningCourse(false));
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2 }}>
      <Stack direction="row" justifyContent="space-between" mb={3}>
        <Typography variant="h4">Mentor Dashboard</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenCreateCourse(true)}
        >
          New Course
        </Button>
      </Stack>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : courses.length === 0 ? (
        <Typography>No courses created yet.</Typography>
      ) : (
        <Grid container spacing={3}>
          {courses.map((course) => {
            const chapters = [...(course.chapters || [])].sort(
              (a, b) => a.sequence_number - b.sequence_number
            );

            return (
              <Grid item xs={12} key={course.id}>
                <Card>
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="h6">{course.title}</Typography>
                      <Stack direction="row">
                        <IconButton
                          onClick={() => {
                            setEditingCourse(course);
                            setCourseTitle(course.title);
                            setCourseDescription(course.description || "");
                            setOpenEditCourse(true);
                          }}
                        >
                          <EditIcon />
                        </IconButton>

                        <IconButton
                          color="error"
                          onClick={() => handleDeleteCourse(course.id)}
                        >
                          <DeleteIcon />
                        </IconButton>

                        <IconButton
                          onClick={() => {
                            setActiveCourse(course);
                            setSelectedStudent("");
                            fetchStudents();
                            setOpenAssign(true);
                          }}
                        >
                          <PersonAddIcon />
                        </IconButton>
                      </Stack>
                    </Stack>

                    <Typography variant="body2" color="text.secondary" mb={2}>
                      {course.description || "No description"}
                    </Typography>

                    <Divider sx={{ mb: 2 }} />

                    <Typography variant="subtitle2">Chapters</Typography>

                    {chapters.length > 0 ? (
                      <Stack spacing={0.5} mb={2}>
                        {chapters.map((ch) => (
                          <Stack
                            key={ch.id}
                            direction="row"
                            justifyContent="space-between"
                          >
                            <Typography variant="body2">
                              {ch.sequence_number}. {ch.title}
                            </Typography>
                            <IconButton
                              size="small"
                              onClick={() => {
                                setViewChapter(ch);
                                setOpenViewChapter(true);
                              }}
                            >
                              <VisibilityIcon fontSize="small" />
                            </IconButton>
                          </Stack>
                        ))}
                      </Stack>
                    ) : (
                      <Typography variant="body2" color="text.secondary" mb={2}>
                        No chapters yet
                      </Typography>
                    )}

                    <Button
                      size="small"
                      startIcon={<AddIcon />}
                      onClick={() => openAddChapterDialog(course)}
                    >
                      Add Chapter
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      )}

      {/* Dialogs */}
      <Dialog open={openCreateCourse} onClose={() => setOpenCreateCourse(false)} fullWidth maxWidth="sm">
        <DialogTitle>Create Course</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField label="Title" value={courseTitle} onChange={(e) => setCourseTitle(e.target.value)} />
            <TextField label="Description" value={courseDescription} onChange={(e) => setCourseDescription(e.target.value)} multiline rows={3} />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCreateCourse(false)}>Cancel</Button>
          <Button variant="contained" disabled={creatingCourse} onClick={handleCreateCourse}>
            {creatingCourse ? "Creating..." : "Create"}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openEditCourse} onClose={() => setOpenEditCourse(false)} fullWidth maxWidth="sm">
        <DialogTitle>Edit Course</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField label="Title" value={courseTitle} onChange={(e) => setCourseTitle(e.target.value)} />
            <TextField label="Description" value={courseDescription} onChange={(e) => setCourseDescription(e.target.value)} multiline rows={3} />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditCourse(false)}>Cancel</Button>
          <Button variant="contained" disabled={updatingCourse} onClick={handleUpdateCourse}>
            {updatingCourse ? "Updating..." : "Update"}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openAddChapter} onClose={() => setOpenAddChapter(false)} fullWidth maxWidth="sm">
        <DialogTitle>Add Chapter</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField label="Title" value={chapterData.title} onChange={(e) => setChapterData({ ...chapterData, title: e.target.value })} />
            <TextField label="Description" value={chapterData.description} onChange={(e) => setChapterData({ ...chapterData, description: e.target.value })} multiline rows={3} />
            <TextField label="Video URL" value={chapterData.video_url} onChange={(e) => setChapterData({ ...chapterData, video_url: e.target.value })} />
            <TextField label="Image URL" value={chapterData.image_url} onChange={(e) => setChapterData({ ...chapterData, image_url: e.target.value })} />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddChapter(false)}>Cancel</Button>
          <Button variant="contained" disabled={addingChapter} onClick={handleAddChapter}>
            {addingChapter ? "Adding..." : "Add"}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openAssign} onClose={() => setOpenAssign(false)} fullWidth maxWidth="sm">
        <DialogTitle>Assign Course</DialogTitle>
        <DialogContent>
          <TextField
            select
            label="Select Student"
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            fullWidth
            sx={{ mt: 2 }}
            disabled={fetchingStudents}
          >
            {students.map((s) => (
              <MenuItem key={s.id} value={s.id}>
                {s.username} ({s.email})
              </MenuItem>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAssign(false)}>Cancel</Button>
          <Button variant="contained" disabled={assigningCourse} onClick={handleAssignCourse}>
            {assigningCourse ? "Assigning..." : "Assign"}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
