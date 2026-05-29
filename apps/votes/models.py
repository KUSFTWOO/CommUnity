from django.db import models
from django.conf import settings
from django.utils import timezone


class Poll(models.Model):
    question = models.CharField(max_length=300)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='polls'
    )
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.question}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def total_votes(self):
        return self.options.aggregate(total=models.Sum('votes_count'))['total'] or 0


class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.CharField(max_length=200)
    votes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['poll']),
        ]

    def __str__(self):
        return f"{self.poll.question} - {self.text}"

    @property
    def percentage(self):
        total = self.poll.total_votes
        if total == 0:
            return 0
        return round((self.votes_count / total) * 100, 1)


class Vote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    option = models.ForeignKey(
        PollOption,
        on_delete=models.CASCADE,
        related_name='user_votes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poll_votes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['poll', 'user']]
        indexes = [
            models.Index(fields=['poll', 'user']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.nickname} voted on Poll {self.poll_id}"
