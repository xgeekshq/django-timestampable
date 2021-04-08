from django.conf import settings
from rest_framework.exceptions import PermissionDenied


def can_hard_delete(view):
    action = getattr(view, 'action', None)

    if action is None:
        from timestamps.drf.mixins import BulkDestroyModelMixin

        if issubclass(view, BulkDestroyModelMixin):
            action = 'bulk_destroy'

    if action == 'bulk_destroy' and not getattr(settings, 'TIMESTAMPS__BULK_HARD_DELETE', False):
        raise PermissionDenied()
