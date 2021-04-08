from django.conf import settings
from rest_framework.exceptions import PermissionDenied


def validate_hard_delete_is_allowed():
    if not getattr(settings, 'ALLOW_PERMANENT_BULK_DELETE', False):
        raise PermissionDenied()
