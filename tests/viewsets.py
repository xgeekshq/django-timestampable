from timestamps.drf.viewsets import SoftDeleteModelViewSet
from .models import Foo
from .serializers import FooSerializer


class FooViewSet(SoftDeleteModelViewSet):
    queryset = Foo.objects.all()
    serializer_class = FooSerializer
