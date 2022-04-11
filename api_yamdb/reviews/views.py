from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend
from .permissions import AdminAllPermission, AdminAllOnlyAuthorPermission
from django.shortcuts import get_object_or_404
from .models import Category, Genre, Titles, Review, Comment
from .serializers import TitlesSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .pagination import CategoryPagination, GenrePagination, TitlesPagination, ReviewPagination

# Create your views here.
class ListCreateDestroyModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class GenreViewSet(ListCreateDestroyModelViewSet):
    """Вьюсет для Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = GenrePagination
    lookup_field = 'slug'



class CategoryViewSet(ListCreateDestroyModelViewSet):
    """Вьюсет для Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = CategoryPagination
    search_fields = ('^name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для Titles"""
    queryset = Titles.objects.annotate(rating=Avg('review__score')).order_by('year')
    serializer_class = TitlesSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = TitlesPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')
    filterset_fields = ('category', 'genre', 'name', 'year')



class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Review"""
    serializer_class = ReviewSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllOnlyAuthorPermission,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = ReviewPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        new_qweryset = Review.objects.filter(title=title)
        return new_qweryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)
    #def perform_create(self, serializer):
        #serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Comment."""
    serializer_class = CommentSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllOnlyAuthorPermission,)

    def get_queryset(self):
        #title_id = self.kwargs.get('title_id')
        #title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        new_qweryset = Comment.objects.filter(review=review)
        return new_qweryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(
            author=self.request.user,
            review=review
        )
