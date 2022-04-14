from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserAuthSerializer
from .serializers import UserConfirmationCodeSerializer


User = get_user_model()


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """Переопределяем создание кода без учета пароля."""
        if user.last_login is None:
            login_timestamp = ''
        else:
            user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(login_timestamp) + str(timestamp)


def code_send(found_user):
    """Возвращение и отправка токена пользователю на email."""
    token = custom_token_generator.make_token(found_user)
    send_mail(
        'YaMDb API.Сервис',
        f'Здравствуйте {found_user.username}! Ваш код: {token}',
        'from@example.com',
        [found_user.email],
        fail_silently=False,
    )
    return token


@api_view(['POST'])
def signup_to_api(request):
    """View-функция отсылающая код подтверждения на email адрес."""
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    # Ищем такого пользователя
    user = User.objects.filter(email=email).first()
    if user:
        # Если пользователь найден
        # Совпадает ли username у user из request
        if user.username != username:
            message = (
                'This \'email\' already exists or wrong '
                'pair \'username\' and \'email\'.'
            )
            return Response(
                {'username': message},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        # Проверяем, при создании нового пользователя,
        # не занят ли username из request
        if User.objects.filter(username=username).exists():
            return Response(
                {'username': 'This \'username\' already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create(**serializer.validated_data)
    # Отправляем код пользователю
    user.confirmation_code = code_send(user)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def issue_a_token(request):
    serializer = UserConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # Проверяем username и confirmation_code
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    request_code = serializer.validated_data['confirmation_code']
    if custom_token_generator.check_token(user, request_code):
        tokenjwt = RefreshToken.for_user(user)
        return Response({'token': str(tokenjwt.access_token)})
    return Response(
        {'detail': 'Wrong \'confirmation_code\'.'},
        status=status.HTTP_400_BAD_REQUEST
    )


custom_token_generator = CustomPasswordResetTokenGenerator()
