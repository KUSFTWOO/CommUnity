import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

user = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
    nickname='Administrator'
)
print("[OK] Superuser created successfully")
print(f"username: admin")
print(f"email: admin@example.com")
print(f"password: admin123")
