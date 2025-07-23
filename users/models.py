from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    # Extend more fields later if needed
    pass

 

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"  # Use this for user.profile
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    region = models.CharField(max_length=100, blank=True)
    language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', 'English'),
            ('hi', 'Hindi'),
            ('bn', 'Bengali'),
            ('mr', 'Marathi'),
        ]
    )
    persona = models.CharField(
        max_length=100,
        choices=[
            ('genz', 'Gen Z'),
            ('elderly', 'Elderly'),
            ('minority', 'Minority Group'),
        ],
        blank=True
    )
    financial_goal = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
