from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # This generates:
    # /api/courses/ (GET list, POST create)
    # /api/courses/my/ (GET custom list for specific user)
    # /api/courses/:id/ (PUT update, DELETE destroy)
    path('', include(router.urls)),
]