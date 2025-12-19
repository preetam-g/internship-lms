import {
  Container,
  Typography,
  Card,
  CardContent,
  Stack,
  Button,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  LinearProgress,
  Box,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import PlayCircleIcon from "@mui/icons-material/PlayCircle";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import LockIcon from "@mui/icons-material/Lock";
import DownloadIcon from "@mui/icons-material/Download";

import { useEffect, useState } from "react";

import {
  getEnrolledCourses,
  getCourseChapters,
  markChapterComplete,
  getMyProgress,
  downloadCertificate,
} from "../../api/apiFunctions";

/* ===========================
   Student Dashboard
=========================== */

export default function StudentDashboard() {
  const [courses, setCourses] = useState([]);
  const [chaptersMap, setChaptersMap] = useState({});
  const [progressMap, setProgressMap] = useState({});
  const [downloadingId, setDownloadingId] = useState(null);

  /* ---------------------------
     Initial Load
  ---------------------------- */
  useEffect(() => {
    fetchCourses();
    fetchProgress();
  }, []);

  const fetchCourses = () => {
    getEnrolledCourses()
      .then((res) => setCourses(res.data.data || []))
      .catch(() => alert("Failed to load courses"));
  };

  const fetchProgress = () => {
    getMyProgress()
      .then((res) => {
        const map = {};
        res.data.data.forEach((p) => {
          map[p.course_id] = p;
        });
        setProgressMap(map);
      })
      .catch(() => alert("Failed to load progress"));
  };

  const fetchChapters = (courseId) => {
    if (chaptersMap[courseId]) return;

    getCourseChapters(courseId)
      .then((res) => {
        const sorted = [...res.data.data].sort(
          (a, b) => a.sequence_number - b.sequence_number
        );
        setChaptersMap((prev) => ({
          ...prev,
          [courseId]: sorted,
        }));
      })
      .catch(() => alert("Failed to load chapters"));
  };

  /* ---------------------------
     Helpers
  ---------------------------- */
  const completedCount = (courseId) =>
    progressMap[courseId]?.completed_chapters || 0;

  const isCompleted = (courseId, index) =>
    index < completedCount(courseId);

  const isLocked = (courseId, index) =>
    index > completedCount(courseId);

  /* ---------------------------
     Mark Chapter Complete
  ---------------------------- */
  const handleComplete = (chapterId) => {
    markChapterComplete(chapterId)
      .then(() => {
        fetchProgress();
      })
      .catch((err) => {
        alert(err?.response?.data?.detail || "Failed to mark complete");
      });
  };

  /* ---------------------------
     Download Certificate
  ---------------------------- */
  const handleDownloadCertificate = (courseId, courseTitle) => {
    setDownloadingId(courseId);

    downloadCertificate(courseId)
      .then((res) => {
        const blob = new Blob([res.data], {
          type: "application/pdf",
        });

        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${courseTitle}-certificate.pdf`;

        document.body.appendChild(link);
        link.click();

        link.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(() => alert("Failed to download certificate"))
      .finally(() => setDownloadingId(null));
  };

  /* ===========================
     UI
  ============================ */
  return (
    <Container maxWidth="md" sx={{ mt: 3 }}>
      <Typography variant="h4" mb={3}>
        Student Dashboard
      </Typography>

      {courses.length === 0 ? (
        <Typography>No enrolled courses.</Typography>
      ) : (
        courses.map((course) => {
          const progress = progressMap[course.id];
          const percentage = progress?.percentage || 0;

          return (
            <Accordion
              key={course.id}
              onChange={(_, expanded) => {
                if (expanded) fetchChapters(course.id);
              }}
              sx={{ mb: 2 }}
            >
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Stack spacing={1} width="100%">
                  <Stack
                    direction="row"
                    justifyContent="space-between"
                    alignItems="center"
                  >
                    <Typography fontWeight={500}>
                      {course.title}
                    </Typography>

                    <Chip
                      label={`${percentage}%`}
                      color={percentage === 100 ? "success" : "primary"}
                    />
                  </Stack>

                  <LinearProgress
                    variant="determinate"
                    value={percentage}
                    color={percentage === 100 ? "success" : "primary"}
                  />
                </Stack>
              </AccordionSummary>

              <AccordionDetails>
                {chaptersMap[course.id]?.map((ch, index) => {
                  const completed = isCompleted(course.id, index);
                  const locked = isLocked(course.id, index);

                  return (
                    <Card
                      key={ch.id}
                      sx={{
                        mb: 1,
                        opacity: locked ? 0.6 : 1,
                      }}
                    >
                      <CardContent>
                        <Stack
                          direction="row"
                          justifyContent="space-between"
                          alignItems="center"
                        >
                          <Stack spacing={0.5}>
                            <Typography variant="subtitle1">
                              {ch.sequence_number}. {ch.title}
                            </Typography>

                            <Button
                              size="small"
                              startIcon={<PlayCircleIcon />}
                              disabled={locked}
                              onx
                              onClick={() =>
                                window.open(ch.video_url, "_blank")
                              }
                            >
                              Watch Video
                            </Button>
                          </Stack>

                          {completed ? (
                            <CheckCircleIcon color="success" />
                          ) : locked ? (
                            <LockIcon color="disabled" />
                          ) : (
                            <Button
                              size="small"
                              variant="contained"
                              onClick={() => handleComplete(ch.id)}
                            >
                              Mark Complete
                            </Button>
                          )}
                        </Stack>
                      </CardContent>
                    </Card>
                  );
                })}

                {/* Certificate Button */}
                {percentage === 100 && (
                  <Box mt={2} textAlign="center">
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<DownloadIcon />}
                      disabled={downloadingId === course.id}
                      onClick={() =>
                        handleDownloadCertificate(
                          course.id,
                          course.title
                        )
                      }
                    >
                      Download Certificate
                    </Button>
                  </Box>
                )}

                <Divider sx={{ mt: 2 }} />
              </AccordionDetails>
            </Accordion>
          );
        })
      )}
    </Container>
  );
}
