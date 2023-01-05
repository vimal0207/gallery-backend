from rest_framework import routers
from .views import UserMediaViewSet

router = routers.DefaultRouter()
router.register('media', UserMediaViewSet)
urlpatterns = router.urls