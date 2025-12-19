from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsMentor, IsCourseMentor, IsStudent
from .models import (
    Course,
    Chapter,
    CourseAssignment,
    ChapterProgress
)
from .serializers import (
    CourseSerializer,
    ChapterSerializer,
    CourseProgressSerializer
)

User = get_user_model()

class CourseViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    Permissions enforced:
    1. User must be Logged In (IsAuthenticated)
    2. User must be a Mentor (IsMentor)
    3. User must be the owner of the course to Edit/Delete (IsCourseMentor)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # IsCourseMentor automatically protects update/destroy actions
    permission_classes = [IsAuthenticated, IsMentor, IsCourseMentor]

    # --- POST /api/courses ---
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Assign logged-in user as mentor
            serializer.save(mentor=request.user)

            return Response({
                'data': serializer.data,
                'detail': 'Course created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- PUT /api/courses/:id ---
    def update(self, request, *args, **kwargs):
        try:
            # get_object() checks IsCourseMentor permission automatically.
            # If user is not the owner, it raises 403 Forbidden immediately.
            instance = self.get_object()

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'data': serializer.data,
                'detail': 'Course updated successfully'
            }, status=status.HTTP_200_OK)

        except Http404:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'detail': 'Unauthorized to update this course'}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            # Handle 403 explicitly if you want a custom message,
            # otherwise DRF returns a default "You do not have permission"
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- DELETE /api/courses/:id ---
    def destroy(self, request, *args, **kwargs):
        try:
            # get_object() checks permission automatically
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail': 'Course deleted successfully'}, status=status.HTTP_200_OK)

        except Http404:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'detail': 'Unauthorized to delete this course'},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': f'Failed to delete: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # --- GET /api/courses/my ---
    @action(detail=False, methods=['get'], url_path='my')
    def my_courses(self, request):
        """
        Return only the courses created by the currently logged-in user.
        """
        try:
            # We filter the queryset manually here to ensure they only see their own
            user_courses = Course.objects.filter(mentor=request.user)
            serializer = self.get_serializer(user_courses, many=True)

            return Response({
                'data': serializer.data,
                'detail': 'Your courses fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # --- POST /api/courses/:id/assign ---
    @action(detail=True, methods=['post'], url_path='assign')
    def assign_course(self, request, pk=None):
        """
        Assign a course to a single student (Mentor Only)
        """
        try:
            # Ensures mentor ownership via IsCourseMentor
            course = self.get_object()

            student_id = request.data.get("student_id")

            if not student_id:
                return Response(
                    {"detail": "student_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            student = get_object_or_404(User, pk=student_id)
            if student.role != User.Role.STUDENT:
                return Response(
                    {"detail": "The selected user is not a Student."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            assignment, created = CourseAssignment.objects.get_or_create(
                course=course,
                student=student
            )

            if not created:
                return Response(
                    {"detail": "Student already assigned to this course"},
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    "detail": "Course assigned successfully",
                    "data": {
                        "course_id": course.id,
                        "student_id": student.id
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except PermissionDenied:
            return Response(
                {"detail": "You are not authorized to assign this course"},
                status=status.HTTP_403_FORBIDDEN
            )

        except Http404:
            return Response(
                {"detail": "Course or Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChapterViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    Handles Chapter Management for a specific course.
    URL: /api/courses/:course_id/chapters/
    """
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, IsMentor]

    def get_course(self):
        """
        Helper to fetch the course and enforce ownership.
        """
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)

        if course.mentor != self.request.user:
            raise PermissionDenied("You are not the mentor of this course.")

        return course

    def list(self, request, *args, **kwargs):
        """
        GET /api/courses/:course_id/chapters
        """
        try:
            course = self.get_course()  # Validates ownership

            # Filter chapters by this course
            chapters = Chapter.objects.filter(course=course)
            serializer = self.get_serializer(chapters, many=True)

            return Response({
                'data': serializer.data,
                'detail': f"""{course.title}: Chapters fetched successfully"""
            }, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        POST /api/courses/:course_id/chapters
        """
        try:
            course = self.get_course()  # Validates ownership

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Save the chapter linked to the fetched course
            serializer.save(course=course)

            return Response({
                'data': serializer.data,
                'detail': 'Chapter added successfully'
            }, status=status.HTTP_201_CREATED)

        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Http404 as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProgressViewSet(viewsets.GenericViewSet):
    """
    Handles Student Progress:
    1. POST /api/progress/:chapter_id/complete/ (Mark complete)
    2. GET  /api/progress/my/                   (View all progress)
    """
    permission_classes = [IsAuthenticated, IsStudent]

    # --- POST /api/progress/:chapter_id/complete ---
    @action(detail=False, methods=['post'], url_path='(?P<chapter_id>[^/.]+)/complete')
    def complete_chapter(self, request, chapter_id=None):
        """
        Mark a chapter as complete.
        Enforces:
        1. Student must be assigned to the course.
        2. Chapters must be completed in strict sequence.
        """
        student = request.user
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        course = chapter.course

        # 1. Validation: Is student assigned to this course?
        if not CourseAssignment.objects.filter(student=student, course=course).exists():
            return Response({
                'detail': 'You are not enrolled in this course.'
            }, status=status.HTTP_403_FORBIDDEN)

        # 2. Validation: Strict Sequence Check
        previous_chapter = Chapter.objects.filter(
            course=course,
            sequence_number__lt=chapter.sequence_number
        ).order_by('-sequence_number').first()

        if previous_chapter:
            # Check if the previous chapter is completed
            is_prev_complete = ChapterProgress.objects.filter(
                student=student,
                chapter=previous_chapter,
                completed=True
            ).exists()

            if not is_prev_complete:
                return Response({
                    'detail': f'You must complete chapter "{previous_chapter.title}" first.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # 3. Mark as Complete
        progress, created = ChapterProgress.objects.get_or_create(
            student=student,
            chapter=chapter
        )

        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
            message = "Chapter marked as completed."
        else:
            message = "Chapter was already completed."

        return Response({
            'detail': message,
            'data': {
                'chapter_id': chapter.id,
                'course_id': course.id,
                'completed': True
            }
        }, status=status.HTTP_200_OK)

    # --- GET /api/progress/my ---
    @action(detail=False, methods=['get'], url_path='my')
    def my_progress(self, request):
        """
        Get overall progress for all enrolled courses.
        Calculates percentage automatically.
        """
        student = request.user

        # Fetch all courses assigned to this student
        # Annotate with total chapters and completed chapters counts
        assignments = CourseAssignment.objects.filter(student=student).select_related('course').annotate(
            total_chapters=Count('course__chapters', distinct=True),
            completed_chapters=Count(
                'course__chapters__chapterprogress',
                filter=Q(course__chapters__chapterprogress__student=student,
                         course__chapters__chapterprogress__completed=True),
                distinct=True
            )
        )

        results = []
        for assign in assignments:
            total = getattr(assign, 'total_chapters', 0)
            completed = getattr(assign, 'completed_chapters', 0)

            percentage = (completed / total * 100) if total > 0 else 0.0

            results.append({
                'course_id': assign.course.id,
                'course_title': assign.course.title,
                'total_chapters': total,
                'completed_chapters': completed,
                'percentage': round(percentage, 2)
            })

        return Response({
            'data': results,
            'detail': 'Progress fetched successfully'
        }, status=status.HTTP_200_OK)