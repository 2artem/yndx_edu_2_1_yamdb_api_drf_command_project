from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import username_validator_not_past_me
from django.contrib.auth.validators import UnicodeUsernameValidator


User = get_user_model()
username_validator = UnicodeUsernameValidator()


class UserAuthSerializer(serializers.Serializer):
    """Сериалайзер для регистрации пользователя."""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[username_validator, username_validator_not_past_me],
    )


class UserConfirmationCodeSerializer(serializers.Serializer):
    """Сериалайзер для выдачи кода пользователю."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[username_validator, username_validator_not_past_me],
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True,
    )
