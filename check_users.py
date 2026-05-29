import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

print("=" * 60)
print("사용자 목록")
print("=" * 60)

users = CustomUser.objects.all().values('nickname', 'email', 'is_deleted')[:10]
for user in users:
    status = "(삭제됨)" if user['is_deleted'] else "(활성)"
    print(f"Nickname: {user['nickname']:20} | Email: {user['email']:30} | {status}")

print("\n" + "=" * 60)
