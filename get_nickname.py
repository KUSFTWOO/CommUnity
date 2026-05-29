#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

user = CustomUser.objects.get(email='user1@example.com')
print(f"Nickname: {user.nickname}")
