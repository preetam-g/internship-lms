
from django.urls import path, include

from apps.users.views import UserListView

urlpatterns = [
 path('api/', include('apps.users.urls')),
 path('api/courses/', include('apps.courses.urls')),
 path('api/progress/', include('apps.progress.urls')),
 path('api/certificates/', include('apps.certificates.urls')),
]
