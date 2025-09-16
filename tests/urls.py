from django.urls import path
from timestamps.drf import routers
from .viewsets import FooViewSet
from .views import BarRetrieveAPIView


router = routers.DefaultRouter()
router.register(r'foos', FooViewSet, basename='foos')

foo_urls = router.urls
bar_urls = [
    path('bars/<uuid:pk>/', BarRetrieveAPIView.as_view()),
]

urlpatterns = foo_urls + bar_urls
