#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

# Create admin account
admin_email = 'admin@example.com'
admin_password = 'admin123'

# Check if admin already exists
if CustomUser.objects.filter(email=admin_email).exists():
    print(f"Admin account '{admin_email}' already exists. Updating password...")
    admin = CustomUser.objects.get(email=admin_email)
    admin.set_password(admin_password)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
    print(f"Admin account updated successfully!")
else:
    print(f"Creating admin account...")
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email=admin_email,
        password=admin_password,
        nickname='Administrator'
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"Admin account created successfully!")

print(f"Email: {admin.email}")
print(f"Password: {admin_password}")
print(f"Is Superuser: {admin.is_superuser}")
print(f"Is Staff: {admin.is_staff}")
