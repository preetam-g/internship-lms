
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    LoginView,
    # UserListView,
    # ApproveMentorView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    # path('users/', UserListView.as_view()),
    # path('users/<int:id>/approve-mentor/', ApproveMentorView.as_view()),
]
