from django.urls import path
from django.urls import include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet


router = SimpleRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
