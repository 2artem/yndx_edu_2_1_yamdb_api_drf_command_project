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


def checking_required_fields(request, chek_list_required_fields):
    """Проверка входящих данных на обязательные поля."""
    message = ['This field is required.']
    dict_required_fields = {}
    for field in chek_list_required_fields:
        if field not in request.data:
            dict_required_fields[field] = message
    if len(dict_required_fields) != 0:
        return Response(
            dict_required_fields,
            status=status.HTTP_400_BAD_REQUEST
        )


def token_send(found_user):
    """Возвращение и отправка токена пользователь на email."""
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
    user = User.objects.filter(username=serializer.validated_data['username'])
    # Есть ли такой username в БД
    if user.exists():
        if user[0].email == email:
            user[0].confirmation_code = token_send(user[0])
            user[0].save()
            return Response(
                {'email': user[0].email, 'username': user[0].username},
                status=status.HTTP_200_OK,
            )
        message = (
            'This '"'email'"' already exists or wrong'
            'pair '"'username'"' and '"'email'"'.'
        )
        return Response(
            {'username': message},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Проверяем что входящий емейл не принадлежит другому пользователю
    if User.objects.filter(email=serializer.validated_data['email']).exists():
        return Response(
            {'email': 'This '"'email'"' already exists.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    new_user = User.objects.create(**serializer.validated_data)
    new_user.confirmation_code = token_send(new_user)
    new_user.save()
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
        {'detail': 'Wrong '"'confirmation_code'"'.'},
        status=status.HTTP_400_BAD_REQUEST
    )


custom_token_generator = CustomPasswordResetTokenGenerator()
