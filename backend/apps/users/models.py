
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        (1, 'admin'), # (db_value, display_value)
        (2, 'mentor'),
        (3, 'student'),
    )

    role = models.CharField(max_length=10, choices=ROLES, default='student')
    is_approved = models.BooleanField(default=False)