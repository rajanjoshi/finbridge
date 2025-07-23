from django.contrib import admin
from .models import DocumentUpload

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_by', 'status', 'uploaded_at')
