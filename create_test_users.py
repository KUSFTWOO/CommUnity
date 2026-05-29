import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser

# 테스트 사용자들
test_users = [
    {
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'user1234',
        'nickname': 'User One',
        'bio': '첫 번째 사용자입니다.',
        'is_staff': False,
    },
    {
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'user2234',
        'nickname': 'User Two',
        'bio': '두 번째 사용자입니다.',
        'is_staff': False,
    },
    {
        'username': 'moderator',
        'email': 'moderator@example.com',
        'password': 'mod2234',
        'nickname': 'Moderator',
        'bio': '커뮤니티 운영자입니다.',
        'is_staff': True,
    },
]

for user_data in test_users:
    password = user_data.pop('password')
    user = CustomUser.objects.create_user(**user_data)
    user.set_password(password)
    user.save()
    print(f"[OK] Created user: {user.nickname} ({user.email})")

print("\n[Summary] 테스트 계정 생성 완료")
