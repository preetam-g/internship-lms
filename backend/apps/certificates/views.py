from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.courses.models import Course, Chapter, ChapterProgress, CourseAssignment
from .utils import generate_certificate_pdf
from apps.courses.permissions import IsStudent

from .models import Certificate

class CertificateViewSet(viewsets.GenericViewSet):
    """
    Handles Certificate Generation and Download.
    GET /api/certificates/:course_id/
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def retrieve(self, request, pk=None):
        """
        GET /api/certificates/:course_id/
        Logic:
        1. Check if user is enrolled.
        2. Check if user has completed ALL chapters (100%).
        3. If certificate exists, return it.
        4. If not, generate it, save it, then return it.
        """
        student = request.user
        course_id = pk

        try:
            course = get_object_or_404(Course, pk=course_id)

            # 1. Check Enrollment (Optional, but good for security)
            if not CourseAssignment.objects.filter(student=student, course=course).exists():
                return Response({'detail': 'Not enrolled'}, status=status.HTTP_403_FORBIDDEN)

            # 2. Check for 100% Completion
            total_chapters = Chapter.objects.filter(course=course).count()

            # if total_chapters == 0:
            #     return Response({'detail': 'Course has no chapters to complete.'}, status=status.HTTP_400_BAD_REQUEST)

            completed_chapters = ChapterProgress.objects.filter(
                student=student,
                chapter__course=course,
                completed=True
            ).count()

            if completed_chapters < total_chapters:
                missing = total_chapters - completed_chapters
                return Response({
                    'detail': f'Course not completed. You have {missing} chapters remaining.',
                    'progress': f'{completed_chapters}/{total_chapters}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Get or Generate Certificate
            certificate, created = Certificate.objects.get_or_create(
                student=student,
                course=course
            )

            # If it was just created (or if file is missing), generate the PDF
            if created or not certificate.pdf_file:
                pdf_file = generate_certificate_pdf(
                    student_name=student.username,
                    course_name=course.title,
                    date_str=certificate.issued_at.strftime("%Y-%m-%d"),
                    cert_id=certificate.certificate_id
                )
                certificate.pdf_file.save(pdf_file.name, pdf_file)
                certificate.save()

            # 4. Return the file as a download
            # FileResponse automatically sets the correct headers for PDF viewing/download
            return FileResponse(
                certificate.pdf_file.open('rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=f"Certificate-{course.title}.pdf"
            )

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)