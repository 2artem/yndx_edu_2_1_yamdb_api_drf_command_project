from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer


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
    # Проверяем наличие обязательных полей
    chek_list_required_fields = ['username', 'email']
    not_correct_fields = checking_required_fields(
        request,
        chek_list_required_fields
    )
    if not_correct_fields is not None:
        return not_correct_fields
    # Запрет на создание 'username'='me'
    if request.data['username'] == 'me':
        return Response(
            {'detail': 'username cannot be '"'me'"'.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Проверяем есть в БД username (значит валидный email будет тоже)
    found_user = User.objects.filter(username=request.data['username'])
    if len(found_user) != 1:
        # username отсутствует, создаем нового
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Отправляем токен
            found_user = User.objects.get(username=request.data['username'])
            found_user.confirmation_code = token_send(found_user)
            found_user.save()
            return Response(
                {'email': found_user.email, 'username': found_user.username},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Проверяем что email соотвтетсвует username в БД,
    # предотврящая несанкционированный доступ
    found_user = User.objects.get(username=request.data['username'])
    if found_user.email != request.data['email']:
        return Response(
            {'detail': 'Wrong pair '"'username'"' and '"'email'"'.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Отправляем токен
    found_user.confirmation_code = token_send(found_user)
    found_user.save()
    return Response(
        {'email': found_user.email, 'username': found_user.username},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def issue_a_token(request):
    # Проверяем наличие обязательных полей
    chek_list_required_fields = ['username', 'confirmation_code']
    not_correct_fields = checking_required_fields(
        request,
        chek_list_required_fields
    )
    if not_correct_fields is not None:
        return not_correct_fields
    # Проверяем username и confirmation_code
    user = get_object_or_404(User, username=request.data['username'])
    request_code = request.data['confirmation_code']
    if custom_token_generator.check_token(user, request_code):
        tokenjwt = RefreshToken.for_user(user)
        return Response({'token': str(tokenjwt.access_token)})
    return Response(
        {'detail': 'Wrong '"'confirmation_code'"'.'},
        status=status.HTTP_400_BAD_REQUEST
    )


custom_token_generator = CustomPasswordResetTokenGenerator()
