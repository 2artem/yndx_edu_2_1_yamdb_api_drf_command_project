from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .pagination import UserPagination
from .serializers import UserSerializer
from .permissions import AdminAllPermissionOrMeURLGetUPDMyself


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с приложением users."""
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)
    permission_classes = (
        permissions.IsAuthenticated,
        AdminAllPermissionOrMeURLGetUPDMyself,
    )

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Метод обрабатывающий эндпоинт 'me'."""
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        # Если username и email не переданы
        request.POST._mutable = True
        request.data['email'] = request.user.email
        request.data['username'] = request.user.username
        request.POST._mutable = False
        # Сериализуем данные
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            # Проверка что роль может изменить только admin или superuser
            if 'role' in request.data:
                if user.is_superuser or user.is_admin:
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'role': 'user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
