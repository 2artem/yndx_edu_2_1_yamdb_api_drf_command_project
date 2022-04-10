from rest_framework import permissions

class AdminAllPermission(permissions.BasePermission):
    """
    Кастомный пермишн для работы администратора c небезопасными методами.
    """

    def has_permission(self, request, view):
        """Переопределяем стандартный метод has_permission."""
        return bool(request.user.is_superuser or request.user.role == 'admin')


class AdminAllOnlyAuthorPermission(permissions.BasePermission):
    """
    Кастомный пермишн для работы администратора
    автора объекта c небезопасными методами.
    """

    def has_object_permission(self, request, view, obj):
        """Переопределяем стандартный метод has_object_permission."""
        return bool(
            request.user.is_superuser
            or request.user.role == 'admin'
            or obj.author == request.user
        )