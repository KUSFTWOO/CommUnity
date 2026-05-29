from django.db import models
from django.conf import settings


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notices'
    )
    is_important = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_important', '-created_at']
        indexes = [
            models.Index(fields=['-is_important', '-created_at']),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])
