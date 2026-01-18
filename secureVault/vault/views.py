import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .models import VaultFile
from .crypto_service import encrypt_file_upload
from .crypto_service import decrypt_file_download
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password




@login_required
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        password = request.POST.get("password")
     

        if not uploaded_file or not password:
            return HttpResponseBadRequest("File and password required")
        if not check_password(password, request.user.password):
            return HttpResponseBadRequest("Incorrect account password") 

       
        encrypted_bytes = encrypt_file_upload(uploaded_file, password)

        
        encrypted_name = f"{uuid.uuid4().hex}.bin"
        encrypted_dir = os.path.join(settings.MEDIA_ROOT, "vault", "encrypted")
        os.makedirs(encrypted_dir, exist_ok=True)

        encrypted_path = os.path.join(encrypted_dir, encrypted_name)

       
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_bytes)

        
        VaultFile.objects.create(
            owner=request.user,
            original_filename=uploaded_file.name,
            encrypted_filename=encrypted_name,
            file_size=len(encrypted_bytes)
        )

        return redirect("vault_dashboard")

    return render(request, "vault/upload.html")

@login_required
def download_file(request, file_id):
    vault_file = get_object_or_404(VaultFile, id=file_id, owner=request.user)

    if request.method == "POST":
        password = request.POST.get("password")
        if not password:
            return HttpResponseBadRequest("Password required")

        if not check_password(password, request.user.password):
            return HttpResponseBadRequest("Incorrect account password")     
        encrypted_path = os.path.join(
            settings.MEDIA_ROOT,
            "vault",
            "encrypted",
            vault_file.encrypted_filename
        )

        if not os.path.exists(encrypted_path):
            return HttpResponseBadRequest("Encrypted file missing")

        
        with open(encrypted_path, "rb") as f:
            encrypted_bytes = f.read()

        
        try:
            decrypted_bytes = decrypt_file_download(encrypted_bytes, password)
        except Exception:
            return HttpResponseBadRequest("Invalid password or corrupted file")

        
        response = HttpResponse(
            decrypted_bytes,
            content_type="application/octet-stream"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{vault_file.original_filename}"'
        )

        return response

    return render(request, "vault/enter_password.html", {"file": vault_file})
@login_required
def vault_dashboard(request):
    """
    Displays the user's vault dashboard with uploaded files.
    """
    files = VaultFile.objects.filter(
        owner=request.user,
        is_deleted=False
    ).order_by("-uploaded_at")

    return render(request, "vault/dashboard.html", {
        "files": files
    })

@login_required
def delete_file(request, file_id):
    vault_file = get_object_or_404(
        VaultFile,
        id=file_id,
        owner=request.user,
        is_deleted=False
    )

    if request.method == "POST":
        vault_file.is_deleted = True
        vault_file.save()
        return redirect("vault_dashboard")

    return HttpResponseBadRequest("Invalid request")
@login_required
def recycle_bin(request):
    deleted_files = VaultFile.objects.filter(
        owner=request.user,
        is_deleted=True
    ).order_by("-uploaded_at")

    return render(request, "vault/recycle_bin.html", {
        "files": deleted_files
    })

@login_required
def permanent_delete(request, file_id):
    vault_file = get_object_or_404(
        VaultFile,
        id=file_id,
        owner=request.user,
        is_deleted=True
    )

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    encrypted_path = os.path.join(
        settings.MEDIA_ROOT,
        "vault",
        "encrypted",
        vault_file.encrypted_filename
    )

    
    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)

    
    vault_file.delete()

    return redirect("recycle_bin")
@login_required
def restore_file(request, file_id):
    vault_file = get_object_or_404(
        VaultFile,
        id=file_id,
        owner=request.user,
        is_deleted=True
    )

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    vault_file.is_deleted = False
    vault_file.save(update_fields=["is_deleted"])

    return redirect("recycle_bin")
