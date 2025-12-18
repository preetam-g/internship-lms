
from django.urls import path
from .views import RegisterView, LoginView, UserListView, ApproveMentorView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:id>/approve-mentor/', ApproveMentorView.as_view()),

]
