from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'title']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    @property
    def is_multiday(self):
        return self.end_date is not None and self.end_date > self.start_date

    @property
    def duration_display(self):
        """일정 기간을 문자열로 표시"""
        if self.end_date:
            if self.start_date == self.end_date:
                return self.start_date.strftime('%Y.%m.%d')
            else:
                return f"{self.start_date.strftime('%Y.%m.%d')} ~ {self.end_date.strftime('%Y.%m.%d')}"
        else:
            return self.start_date.strftime('%Y.%m.%d')
