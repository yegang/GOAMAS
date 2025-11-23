from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import AlertContent

#@receiver(post_migrate)
def create_custom_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(AlertContent)
    print("ContentType:", content_type)

    permission, created = Permission.objects.get_or_create(
        codename='can_import_data',
        name='Can Import Data',
        content_type=content_type,
    )
    print("Can Import Data Permission Created:", created)

    permission, created = Permission.objects.get_or_create(
        codename='can_export_data',
        name='Can Export Data',
        content_type=content_type,
    )
    print("Can Export Data Permission Created:", created)