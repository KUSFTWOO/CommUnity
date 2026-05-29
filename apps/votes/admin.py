from django.contrib import admin
from .models import Poll, PollOption, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'expires_at', 'total_votes', 'created_at')
    list_filter = ('expires_at', 'created_at')
    search_fields = ('question',)
    readonly_fields = ('created_at', 'total_votes')
    fieldsets = (
        ('기본 정보', {'fields': ('question', 'created_by')}),
        ('마감 정보', {'fields': ('expires_at',)}),
        ('통계', {'fields': ('total_votes', 'created_at')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'text', 'votes_count', 'percentage', 'created_at')
    list_filter = ('poll', 'created_at')
    search_fields = ('poll__question', 'text')
    readonly_fields = ('votes_count', 'created_at', 'percentage')
    fieldsets = (
        ('선택지 정보', {'fields': ('poll', 'text')}),
        ('투표 결과', {'fields': ('votes_count', 'percentage')}),
        ('생성 정보', {'fields': ('created_at',)}),
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'option', 'created_at')
    list_filter = ('poll', 'created_at')
    search_fields = ('user__username', 'user__nickname', 'poll__question')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('투표 정보', {'fields': ('poll', 'option', 'user')}),
        ('생성 정보', {'fields': ('created_at',)}),
    )
