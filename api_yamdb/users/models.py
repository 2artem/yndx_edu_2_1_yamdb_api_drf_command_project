from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


def username_validator_not_past_me(value):
    """Проверка что username не равно me."""
    message = (
        'В сервисе YaMDb API запрещено использовать '
        'значение '"'me'"' как имя пользователя.'
    )
    if value == 'me':
        raise ValidationError(message)


class User(AbstractUser):
    """Кастомная модель юзера"""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, username_validator_not_past_me],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        null=True,
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)
    bio = models.TextField(
        'Биография',
        max_length=150,
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLE,
        default=USER,
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения email',
        max_length=150,
        blank=True,
        null=True,
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
