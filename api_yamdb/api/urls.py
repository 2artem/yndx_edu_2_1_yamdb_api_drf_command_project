from django.urls import path
from .views import signup_to_api
from .views import issue_a_token


urlpatterns = [
    path('v1/auth/signup/', signup_to_api),
    path('v1/auth/token/', issue_a_token),
]
