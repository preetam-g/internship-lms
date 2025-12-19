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
from ..users.permissions import IsAdminRole

User = get_user_model()

class CourseViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """
    Course Management API

    Roles:
    - Admin:
        * List all courses
    - Mentor:
        * Create courses
        * Update/Delete own courses
        * View own courses
        * Assign students to own courses
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # -------------------------------------------------
    # Dynamic permissions (CRITICAL)
    # -------------------------------------------------
    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated(), IsAdminRole()]

        if self.action in ["create", "my_courses"]:
            return [IsAuthenticated(), IsMentor()]

        if self.action in ["update", "partial_update", "destroy", "assign_course"]:
            return [IsAuthenticated(), IsMentor(), IsCourseMentor()]

        if self.action == "enrolled_courses":
            return [IsAuthenticated(), IsStudent()]

        return [IsAuthenticated()]

    # -------------------------------------------------
    # GET /api/courses/  (Admin only)
    # -------------------------------------------------
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "data": serializer.data,
                "detail": "All courses fetched successfully"
            },
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------
    # POST /api/courses/  (Mentor)
    # -------------------------------------------------
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Logged-in mentor becomes course owner
        serializer.save(mentor=request.user)

        return Response(
            {
                "data": serializer.data,
                "detail": "Course created successfully"
            },
            status=status.HTTP_201_CREATED
        )

    # -------------------------------------------------
    # PUT /api/courses/:id/  (Mentor + owner)
    # -------------------------------------------------
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "data": serializer.data,
                "detail": "Course updated successfully"
            },
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------
    # DELETE /api/courses/:id/  (Mentor + owner)
    # -------------------------------------------------
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Course deleted successfully"},
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------
    # GET /api/courses/my/  (Mentor)
    # -------------------------------------------------
    @action(detail=False, methods=["get"], url_path="my")
    def my_courses(self, request):
        user_courses = Course.objects.filter(
            mentor=request.user
        )
        serializer = self.get_serializer(
            user_courses,
            many=True
        )

        return Response(
            {
                "data": serializer.data,
                "detail": "Your courses fetched successfully"
            },
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------
    # POST /api/courses/:id/assign/  (Mentor + owner)
    # -------------------------------------------------
    @action(detail=True, methods=["post"], url_path="assign")
    def assign_course(self, request, pk=None):
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

    @action(detail=False, methods=["get"], url_path="enrolled")
    def enrolled_courses(self, request):
        """
        GET /api/courses/enrolled/
        Student can view only courses they are assigned to.
        """
        student = request.user

        courses = Course.objects.filter(
            courseassignment__student = student
        ).distinct()

        serializer = self.get_serializer(courses, many=True)

        return Response(
            {
                "data": serializer.data,
                "detail": "Enrolled courses fetched successfully"
            },
            status=status.HTTP_200_OK
        )


class ChapterViewSet(mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    """
    Handles Chapter Management for a specific course.

    URL:
      /api/courses/:course_id/chapters/

    Access:
    - Mentor (owner):
        * GET chapters
        * POST chapters
    - Student (enrolled):
        * GET chapters only
    """

    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]

    def get_course(self):
        course_id = self.kwargs.get("course_id")
        return get_object_or_404(Course, pk=course_id)

    def is_student_enrolled(self, student, course):
        return CourseAssignment.objects.filter(
            student=student,
            course=course
        ).exists()

    # -------------------------------------------------
    # GET /api/courses/:course_id/chapters/
    # -------------------------------------------------
    def list(self, request, *args, **kwargs):
        """
        Mentor: must own the course
        Student: must be enrolled
        """
        course = self.get_course()
        user = request.user

        # --- Mentor access ---
        if user.role == User.Role.MENTOR:
            if course.mentor != user:
                raise PermissionDenied("You are not the mentor of this course.")

        # --- Student access ---
        elif user.role == User.Role.STUDENT:
            if not self.is_student_enrolled(user, course):
                raise PermissionDenied("You are not enrolled in this course.")

        else:
            raise PermissionDenied("You are not allowed to view chapters.")

        chapters = Chapter.objects.filter(course=course).order_by("sequence_number")
        serializer = self.get_serializer(chapters, many=True)

        return Response(
            {
                "data": serializer.data,
                "detail": "Chapters fetched successfully"
            },
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------
    # POST /api/courses/:course_id/chapters/
    # -------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Mentor-only: must own the course
        """
        user = request.user

        if user.role != User.Role.MENTOR:
            raise PermissionDenied("Only mentors can add chapters.")

        course = self.get_course()

        if course.mentor != user:
            raise PermissionDenied("You are not the mentor of this course.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)

        return Response(
            {
                "data": serializer.data,
                "detail": "Chapter added successfully"
            },
            status=status.HTTP_201_CREATED
        )



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
                    'detail': 'You must complete all previous chapters.'
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