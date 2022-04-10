from django.urls import path
from django.urls import include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet
from .views import signup_to_api
from .views import issue_a_token

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup_to_api),
    path('v1/auth/token/', issue_a_token),
]
