from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from datetime import datetime

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True, validators=[validate_slug])

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True, validators=[validate_slug])

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'

    def __str__(self):
        return self.slug


class Titles(models.Model):
    def check_value_year_valid(value):
        """Проверка что значение года корректно."""
        message = (
            'Невозможно выбрать ненаступивший год для произведения.'
        )
        year_now = datetime.now().year
        if value > year_now:
            raise ValidationError(message)

    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(
        blank=False,
        null=False,
        validators=[check_value_year_valid],
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    CHOICE = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    ]
    text = models.TextField(
        max_length=1000,
        blank=False,
        null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='reviews'
    )
    score = models.IntegerField(choices=CHOICE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        constraints = [
        models.UniqueConstraint(
            name="unique_relationships",
            fields=['author', 'title'],
        ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, 
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='comments'
    )
    text = models.TextField(max_length=10000)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
