
from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
