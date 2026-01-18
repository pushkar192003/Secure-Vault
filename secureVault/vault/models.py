from django.db import models

from django.db import models
from django.contrib.auth.models import User
import uuid

class VaultFile(models.Model):
   
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

   
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vault_files"
    )

   
    original_filename = models.CharField(
        max_length=255
    )

   
    encrypted_filename = models.CharField(
        max_length=255,
        unique=True
    )

    
    encrypted_file = models.FileField(
        upload_to="vault/encrypted/"
    )

    
    file_size = models.BigIntegerField(
        help_text="Size of original file in bytes"
    )


  
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.original_filename} ({self.owner.username})"
