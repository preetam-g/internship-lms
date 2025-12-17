
from django.urls import path
from .views import CertificateView
urlpatterns = [ path('<int:course_id>', CertificateView.as_view()) ]
