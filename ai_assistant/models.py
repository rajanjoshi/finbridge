from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
    ]
    REGION_CHOICES = [
        ('IN', 'India'),
        ('US', 'USA'),
    ]
    PERSONA_CHOICES = [
        ('genz', 'Gen Z'),
        ('elderly', 'Elderly'),
        ('minority', 'Minority Group'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user_profile_assistant" )
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    region = models.CharField(max_length=10, choices=REGION_CHOICES, default='IN')
    persona = models.CharField(max_length=10, choices=PERSONA_CHOICES, default='genz')

    def __str__(self):
        return f"{self.user.username} Profile"
