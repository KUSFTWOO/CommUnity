from django.db import models
from django.conf import settings
from django.utils import timezone


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='surveys'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def total_responses(self):
        return self.responses.count()


class Question(models.Model):
    QUESTION_TYPES = [
        ('TEXT', '주관식 (짧은 답변)'),
        ('TEXTAREA', '주관식 (긴 답변)'),
        ('CHOICE', '객관식 (단일선택)'),
        ('MULTIPLE', '객관식 (복수선택)'),
        ('SCALE', '척도 (1-5)'),
    ]

    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    required = models.BooleanField(default=True)
    options = models.TextField(blank=True, help_text='CHOICE/MULTIPLE의 경우 줄바꿈으로 구분')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['survey']),
        ]

    def __str__(self):
        return f"{self.survey.title} - {self.text}"

    @property
    def parsed_options(self):
        if not self.options:
            return []
        return [opt.strip() for opt in self.options.split('\n') if opt.strip()]


class Response(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    respondent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='survey_responses'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['survey', 'respondent']]
        indexes = [
            models.Index(fields=['survey', 'respondent']),
        ]

    def __str__(self):
        respondent_name = self.respondent.nickname if self.respondent else '익명'
        return f"{self.survey.title} - {respondent_name}"


class Answer(models.Model):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['response']),
            models.Index(fields=['question']),
        ]

    def __str__(self):
        return f"{self.question.text} - {self.answer_text[:50]}"
