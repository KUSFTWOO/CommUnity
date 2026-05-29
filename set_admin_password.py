#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

# admin 계정 조회 및 비밀번호 설정
admin = CustomUser.objects.get(email='admin@example.com')
admin.set_password('admin123')
admin.save()
print(f"Admin account password updated: {admin.email}")
