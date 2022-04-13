from django.core.validators import validate_slug
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from .validators import check_value_year_valid

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=250, unique=True)
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
        db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
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
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title,
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

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'

    def str(self):
        return self.text[:15]
