from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView


urlpatterns = [
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
    path('api/', include('reviews.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
