from rest_framework import viewsets

from .mixins import (
    ListDeletedModelMixin,
    ListWithDeletedModelMixin,
    RetrieveDeletedModelMixin,
    RetrieveWithDeletedModelMixin,
    RestoreModelMixin,
    BulkRestoreModelMixin,
    DestroyModelMixin,
    BulkDestroyModelMixin
)


class ModelViewSet(ListDeletedModelMixin,
                   ListWithDeletedModelMixin,
                   RetrieveDeletedModelMixin,
                   RetrieveWithDeletedModelMixin,
                   RestoreModelMixin,
                   BulkRestoreModelMixin,
                   DestroyModelMixin,
                   BulkDestroyModelMixin,
                   viewsets.ModelViewSet):
    pass
