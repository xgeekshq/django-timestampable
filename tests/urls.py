from django.urls import path
from timestamps.drf import routers
from .viewsets import FooViewSet
from .views import BarRetrieveAPIView


router = routers.DefaultRouter()
router.register(r'foos', FooViewSet, basename='foos')

foourls = router.urls
barurls = [ path('bars/<uuid:pk>/', BarRetrieveAPIView.as_view()), ]

urlpatterns = foourls + barurls
