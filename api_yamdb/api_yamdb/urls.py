from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# Раскомментировать для api/v1/
urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
