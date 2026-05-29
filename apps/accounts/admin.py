from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'nickname', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'nickname', 'username']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인정보', {'fields': ('username', 'first_name', 'last_name', 'nickname', 'bio', 'profile_image')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('보안', {'fields': ('login_fail_count', 'locked_until')}),
        ('삭제', {'fields': ('is_deleted',)}),
        ('중요 날짜', {'fields': ('last_login', 'date_joined')}),
    )
