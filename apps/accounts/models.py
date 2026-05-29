from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    """확장된 사용자 모델"""
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/', blank=True, null=True)

    # 로그인 보안
    login_fail_count = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    # 소프트 삭제
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nickname']

    class Meta:
        db_table = 'accounts_customuser'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['nickname']),
        ]

    def __str__(self):
        return f"{self.nickname} ({self.email})"

    def is_account_locked(self):
        """계정이 잠겨있는지 확인"""
        if self.locked_until and timezone.now() < self.locked_until:
            return True
        return False

    def unlock_account(self):
        """계정 잠금 해제"""
        self.locked_until = None
        self.login_fail_count = 0
        self.save(update_fields=['locked_until', 'login_fail_count'])

    def increment_login_fail(self):
        """로그인 실패 횟수 증가"""
        self.login_fail_count += 1
        if self.login_fail_count >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        self.save(update_fields=['login_fail_count', 'locked_until'])

    def reset_login_fail(self):
        """로그인 실패 횟수 초기화"""
        self.login_fail_count = 0
        self.locked_until = None
        self.save(update_fields=['login_fail_count', 'locked_until'])
