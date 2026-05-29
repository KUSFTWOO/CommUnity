from django.contrib import admin
from .models import Survey, Question, Response, Answer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'expires_at', 'is_anonymous', 'total_responses', 'created_at')
    list_filter = ('expires_at', 'is_anonymous', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'total_responses')
    fieldsets = (
        ('기본 정보', {'fields': ('title', 'description', 'created_by')}),
        ('설정', {'fields': ('is_anonymous', 'expires_at')}),
        ('통계', {'fields': ('total_responses', 'created_at')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'text', 'question_type', 'required', 'order')
    list_filter = ('survey', 'question_type', 'required')
    search_fields = ('survey__title', 'text')
    fieldsets = (
        ('기본 정보', {'fields': ('survey', 'text', 'question_type')}),
        ('설정', {'fields': ('required', 'order')}),
        ('선택지', {'fields': ('options',), 'description': 'CHOICE/MULTIPLE 타입의 경우 줄바꿈으로 구분'}),
    )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'respondent', 'submitted_at')
    list_filter = ('survey', 'submitted_at')
    search_fields = ('survey__title', 'respondent__username', 'respondent__nickname')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('응답 정보', {'fields': ('survey', 'respondent')}),
        ('생성 정보', {'fields': ('submitted_at',)}),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'answer_text')
    list_filter = ('question__survey', 'question')
    search_fields = ('question__text', 'answer_text')
    fieldsets = (
        ('답변 정보', {'fields': ('response', 'question')}),
        ('내용', {'fields': ('answer_text',)}),
    )
