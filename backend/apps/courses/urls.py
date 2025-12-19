from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ChapterViewSet, ProgressViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'progress', ProgressViewSet, basename='progress')

urlpatterns = [
    # Standard Course URLs
    path('', include(router.urls)),

    # Nested Chapter URLs
    # This maps /api/courses/<id>/chapters/ to the ChapterViewSet
    path('courses/<int:course_id>/chapters/', ChapterViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='course-chapters'),
]