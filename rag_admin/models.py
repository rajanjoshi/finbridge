from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class DocumentUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
