from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid

class VaultFile(models.Model):
    # 1. Secure primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 2. File ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vault_files"
    )

    # 3. User-visible filename
    original_filename = models.CharField(
        max_length=255
    )

    # 4. System-level encrypted filename
    encrypted_filename = models.CharField(
        max_length=255,
        unique=True
    )

    # 5. Actual encrypted file storage
    encrypted_file = models.FileField(
        upload_to="vault/encrypted/"
    )

    # 6. Metadata
    file_size = models.BigIntegerField(
        help_text="Size of original file in bytes"
    )


    # 7. Timestamps
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    # 8. Soft delete flag
    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.original_filename} ({self.owner.username})"
