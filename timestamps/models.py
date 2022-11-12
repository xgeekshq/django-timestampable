from django.db import models
from django.utils import timezone
from .managers import SoftDeleteManager


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

    def delete(self, using=None, keep_parents=False, hard: bool = False):
        if hard:
            return super().delete(using, keep_parents)

        self.deleted_at = timezone.now()
        return self.save()

    def restore(self):
        self.deleted_at = None
        return self.save()


class Model(Timestampable, SoftDeletes, models.Model):
    class Meta:
        abstract = True
