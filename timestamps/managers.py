from django.db.models import Manager
from .querysets import SoftDeleteQuerySet


class SoftDeleteManager(Manager):
    def __init__(self, *args, **kwargs):
        self.with_deleted = kwargs.pop('with_deleted', False)
        self.only_deleted = kwargs.pop('only_deleted', False)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.with_deleted:
            return SoftDeleteQuerySet(self.model)

        if self.only_deleted:
            return SoftDeleteQuerySet(self.model).only_deleted()

        return SoftDeleteQuerySet(self.model).without_deleted()

    def delete(self, hard: bool = False):
        return self.get_queryset().delete(hard=hard)
    
    def soft_delete(self):
        return self.delete(hard=False)
    
    def hard_delete(self):
        return self.delete(hard=True)

    def restore(self):
        return self.get_queryset().restore()
