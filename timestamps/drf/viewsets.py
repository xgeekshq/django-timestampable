from rest_framework import viewsets

from .mixins import (
    ListDeletedModelMixin,
    ListWithDeletedModelMixin,
    RetrieveDeletedModelMixin,
    RestoreModelMixin,
    BulkRestoreModelMixin,
    DestroyModelMixin,
    BulkDestroyModelMixin
)


class SoftDeleteModelViewSet(ListDeletedModelMixin,
                             ListWithDeletedModelMixin,
                             RetrieveDeletedModelMixin,
                             RestoreModelMixin,
                             BulkRestoreModelMixin,
                             DestroyModelMixin,
                             BulkDestroyModelMixin,
                             viewsets.ModelViewSet):
    pass
