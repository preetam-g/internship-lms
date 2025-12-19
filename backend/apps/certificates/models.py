from django.db import models
from django.conf import settings
import uuid
from apps.courses.models import Course

class Certificate(models.Model):
    # Unique ID for verification (e.g., printed on the PDF)
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)

    class Meta:
        # A student gets only ONE certificate per course
        unique_together = ('student', 'course')

    def __str__(self):
        return f"Certificate: {self.student.username} - {self.course.title}"