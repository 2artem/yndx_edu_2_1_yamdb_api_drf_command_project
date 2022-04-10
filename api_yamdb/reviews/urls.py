from django.urls import path, include
from rest_framework import routers
from .views import GenreViewSet, CategoryViewSet, CommentViewSet, TitlesViewSet, ReviewViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
