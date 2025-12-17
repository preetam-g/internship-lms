
from django.urls import path, include
urlpatterns = [
 path('api/auth/', include('apps.users.urls')),
 path('api/courses/', include('apps.courses.urls')),
 path('api/progress/', include('apps.progress.urls')),
 path('api/certificates/', include('apps.certificates.urls')),
]
