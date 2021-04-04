from django.db.models import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    def only_deleted(self):
        return self.filter(deleted_at__isnull=False)

    def without_deleted(self):
        return self.filter(deleted_at__isnull=True)

    #  bulk deleting
    def delete(self, hard: bool = False):
        if hard:
            return super(SoftDeleteQuerySet, self).delete()

        return super(SoftDeleteQuerySet, self).update(deleted_at=timezone.now())

    #  bulk restore
    def restore(self):
        return super(SoftDeleteQuerySet, self).update(deleted_at=None)
