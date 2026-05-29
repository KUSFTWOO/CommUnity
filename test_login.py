#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

# admin 계정 확인
admin = CustomUser.objects.get(email='admin@example.com')
print(f"Admin Account: {admin.email}")
print(f"Nickname: {admin.nickname}")
print(f"Is Superuser: {admin.is_superuser}")
print(f"Is Staff: {admin.is_staff}")
print(f"Password Check: {admin.check_password('admin123')}")
