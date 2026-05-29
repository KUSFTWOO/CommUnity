import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

admin = CustomUser.objects.filter(is_staff=True).first()
if admin:
    print(f"Admin exists: {admin.email}")
else:
    print("Creating test admin...")
    user = CustomUser.objects.create_superuser(
        email="admin@test.com",
        username="admin",
        nickname="admin",
        password="admin123"
    )
    print(f"Created admin: {user.email} with password: admin123")
