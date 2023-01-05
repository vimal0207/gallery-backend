from rest_framework import routers
from .views import UserViewSet, MyTokenObtainPairView
from django.urls import path

router = routers.DefaultRouter()
router.register('user', UserViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('auth/', MyTokenObtainPairView.as_view(), name='token_obtain_pair')
]