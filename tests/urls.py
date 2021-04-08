from timestamps.drf import routers
from .viewsets import FooViewSet


router = routers.DefaultRouter()
router.register(r'', FooViewSet)


urlpatterns = router.urls
