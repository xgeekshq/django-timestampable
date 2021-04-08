from django.conf import settings
from rest_framework.exceptions import PermissionDenied


def validate_hard_delete_is_allowed():
    if not getattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', False):
        raise PermissionDenied()
