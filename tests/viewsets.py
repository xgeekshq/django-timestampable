from timestamps.drf.viewsets import ModelViewSet
from .models import Foo
from .serializers import FooSerializer


class FooViewSet(ModelViewSet):
    queryset = Foo.objects.all()
    serializer_class = FooSerializer
