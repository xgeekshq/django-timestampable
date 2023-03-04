from django.db import models, router
from django.utils import timezone
from .managers import SoftDeleteManager
from . import signals

class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeletes(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    objects_deleted = SoftDeleteManager(only_deleted=True)
    objects_with_deleted = SoftDeleteManager(with_deleted=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents: bool = False, hard: bool = False) -> None:
        if hard:
            return super().delete(using, keep_parents)

        using = using or router.db_for_write(self.__class__, instance=self)

        signals.pre_soft_delete.send(
            sender=self.__class__,
            instance=self,
            using=using
        )
        
        self.deleted_at = timezone.now()
        self.save()

        signals.post_soft_delete.send(
            sender=self.__class__,
            instance=self,
            using=using
        )

    def soft_delete(self) -> None:
        self.delete(hard=False)
    
    def hard_delete(self, using=None, keep_parents: bool = False):
        return self.delete(using, keep_parents, hard=True)

    def restore(self) -> None:
        signals.pre_restore.send(sender=self.__class__, instance=self)

        self.deleted_at = None
        self.save()

        signals.post_restore.send(sender=self.__class__, instance=self)


class Model(Timestampable, SoftDeletes, models.Model):
    class Meta:
        abstract = True
