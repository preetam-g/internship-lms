
from django.urls import path
from .views import ProgressView
urlpatterns = [ path('my', ProgressView.as_view()) ]
