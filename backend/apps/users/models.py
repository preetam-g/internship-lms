
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        MENTOR = 2, 'Mentor'
        STUDENT = 3, 'Student'

    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.STUDENT)
    is_approved = models.BooleanField(default=False)