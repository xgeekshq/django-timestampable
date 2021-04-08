import aspectlib

from django.conf import settings
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from timestamps.drf.utils import is_hard_delete_request


class ListDeletedModelMixin:
    def list_deleted(self, request, *args, **kwargs):
        return ListModelMixin.list(self, request, *args, **kwargs)


class ListWithDeletedModelMixin:
    def list_with_deleted(self, request, *args, **kwargs):
        return ListModelMixin.list(self, request, *args, **kwargs)


class RetrieveDeletedModelMixin:
    def retrieve_deleted(self, request, *args, **kwargs):
        return RetrieveModelMixin.retrieve(self, request, *args, **kwargs)


class RetrieveWithDeletedModelMixin:
    def retrieve_with_deleted(self, request, *args, **kwargs):
        return RetrieveModelMixin.retrieve(self, request, *args, **kwargs)


class RestoreModelMixin:
    def restore(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_restore(instance)

        return Response(self.get_serializer(instance=instance).data)

    def perform_restore(self, instance):
        return instance.restore()


class BulkRestoreModelMixin:
    def bulk_restore(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = self.perform_bulk_restore(queryset)

        if getattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', False):
            return Response(data={'count': count, }, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_bulk_restore(self, qs):
        return qs.restore()


class DestroyModelMixin(mixins.DestroyModelMixin):
    def perform_destroy(self, instance):
        return instance.delete(hard=is_hard_delete_request(self))


class BulkDestroyModelMixin:
    def perform_bulk_destroy(self, qs):
        return qs.delete(hard=is_hard_delete_request(self))

    def bulk_destroy(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        count = self.perform_bulk_destroy(queryset)

        if not getattr(settings, 'TIMESTAMPS__BULK_RESPONSE_CONTENT', False):
            return Response(status=status.HTTP_204_NO_CONTENT)

        # a delete operation (hard delete) returns a tuple of:
        # - total rows deleted (count)
        # - total rows deleted per table (per_model)
        if isinstance(count, tuple):
            count, count_per_model = count
            return Response(data={'count': count, 'count_per_model': count_per_model, }, status=status.HTTP_200_OK)

        return Response(data={'count': count}, status=status.HTTP_200_OK)


def __remove_clause_deleted_at(queryset):
    from timestamps.querysets import SoftDeleteQuerySet
    from django.db.models.lookups import IsNull

    if not isinstance(queryset, SoftDeleteQuerySet):
        return queryset

    queryset = queryset.all()  # clone
    where = queryset.query.where

    for i, child in enumerate(where.children):
        if isinstance(child, IsNull) and child.lhs.field.name == 'deleted_at':
            where.children.pop(i)
            break

    return queryset


# Using Aspect-Oriented Programming (AOP)
# to change behavior of GenericAPIView.get_queryset(self).
# Doing this way, there is no need to pollute CoreModelViewSet
# and gives to developers the possibility
# to use only a subset of Mixins of soft deleting technology,
# without the need to use all the views mixins, extended in CoreModelViewSet.
@aspectlib.Aspect
def __get_queryset(*args, **kwargs):
    queryset = yield aspectlib.Proceed

    view = args[0]

    mixin = {
        'list_with_deleted': ListWithDeletedModelMixin,
        'retrieve_with_deleted': RetrieveWithDeletedModelMixin,
    }

    if is_hard_delete_request(view):
        mixin['destroy'] = DestroyModelMixin
        mixin['bulk_destroy'] = BulkDestroyModelMixin

    mixin = mixin.get(view.action, None)

    if mixin and isinstance(view, mixin):
        queryset = __remove_clause_deleted_at(queryset)
        yield aspectlib.Return(queryset)

    mixin = {
        'list_deleted': ListDeletedModelMixin,
        'retrieve_deleted': RetrieveDeletedModelMixin,
        'restore': RestoreModelMixin,
        'bulk_restore': BulkRestoreModelMixin,
    }.get(view.action, None)

    if mixin and isinstance(view, mixin):
        queryset = __remove_clause_deleted_at(queryset)
        yield aspectlib.Return(queryset.only_deleted())

    yield aspectlib.Return(queryset)


aspectlib.weave(target=GenericAPIView.get_queryset, aspects=__get_queryset)
