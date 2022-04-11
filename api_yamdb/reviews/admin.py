from django.contrib import admin
from .models import Review
from .models import Title
from .models import Genre
from .models import Category
from .models import Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'score',
        'pub_date',
        'title'
    )


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'description',
        'year'
    )
    filter_horizontal = ('genre',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date'
    )


admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
