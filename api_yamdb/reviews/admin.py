from django.contrib import admin
from .models import Review, Titles, Genre, Category, Comment

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'score',
        'pub_date',
        'title'
    )

admin.site.register(Review, ReviewAdmin)


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        #'rating',
        #'genre',
        'category',
        'description',
        'year'
    )
    filter_horizontal = ('genre',)

admin.site.register(Titles, TitlesAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )

admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date'
    )

admin.site.register(Comment, CommentAdmin)
