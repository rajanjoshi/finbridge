from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DocumentUploadForm
from .models import DocumentUpload
from .utils import upload_to_vertex_rag, sync_to_rag

@login_required
def upload_document(request):
    status_msg = None

    if request.method == "POST":
        if "upload_file" in request.POST:
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                doc = form.save(commit=False)
                doc.uploaded_by = request.user
                doc.save()
                success = upload_to_vertex_rag(doc.file.path)
                doc.status = "Uploaded" if success else "Failed"
                doc.save()
                status_msg = "✅ File uploaded and sent to GCS." if success else "❌ Upload failed."
        elif "sync_rag" in request.POST:
            result = sync_to_rag()
            status_msg = "✅ Vertex RAG sync complete." if result else "❌ Sync failed."

    form = DocumentUploadForm()
    uploads = DocumentUpload.objects.all().order_by("-uploaded_at")
    return render(request, "rag_admin/upload.html", {
        "form": form,
        "uploads": uploads,
        "status_msg": status_msg,
    })
