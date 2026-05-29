#!/usr/bin/env python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

# 모든 사용자 조회
all_users = CustomUser.objects.all()
print(f"Total users: {all_users.count()}")
print("\n=== All Users ===")
for user in all_users:
    is_admin = "Yes" if user.is_superuser else "No"
    is_staff = "Yes" if user.is_staff else "No"
    print(f"  - {user.email} (Superuser: {is_admin}, Staff: {is_staff})")

# 관리자 계정 조회
superusers = CustomUser.objects.filter(is_superuser=True)
print(f"\n=== Admin Accounts ===")
if superusers.exists():
    print(f"Admin count: {superusers.count()}")
    for user in superusers:
        print(f"  - {user.email}")
else:
    print("No admin accounts found.")
