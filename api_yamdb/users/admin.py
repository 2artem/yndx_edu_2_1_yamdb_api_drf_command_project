from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Кастомная Админка"""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'is_staff',
        'is_superuser',
        'confirmation_code',
    )
    search_fields = ('username',)
    empty_value_display = 'NULL'


admin.site.register(User, UserAdmin)
