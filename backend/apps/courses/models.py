from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_created"
    )
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="chapters/images/", null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    sequence_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("course", "sequence_number")
        ordering = ["course", "sequence_number"]

    def __str__(self):
        return f"{self.course.title}: {self.sequence_number} - {self.title}"


class CourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_courses"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")


class ChapterProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "chapter")
