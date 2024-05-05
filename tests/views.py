from rest_framework import generics
from .models import Bar
from .serializers import BarSerializer


class BarRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer

