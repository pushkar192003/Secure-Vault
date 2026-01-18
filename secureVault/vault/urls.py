from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.vault_dashboard, name="vault_dashboard"),
    path("upload/", views.upload_file, name="upload_file"),
    path("download/<uuid:file_id>/", views.download_file, name="download_file"),
    path("delete/<uuid:file_id>/", views.delete_file, name="delete_file"),
    path("recycle-bin/", views.recycle_bin, name="recycle_bin"),
    path("restore/<uuid:file_id>/", views.restore_file, name="restore_file"),
    path("delete-permanent/<uuid:file_id>/", views.permanent_delete, name="permanent_delete"),
]
