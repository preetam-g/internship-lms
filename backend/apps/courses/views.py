from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsMentor, IsCourseMentor
from .models import (
    Course,
    Chapter
)
from .serializers import (
    CourseSerializer,
    ChapterSerializer
)


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