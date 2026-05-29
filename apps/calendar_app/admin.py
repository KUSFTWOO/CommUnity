from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'created_by', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'start_date', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'description', 'created_by')
        }),
        ('일정', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('상태', {
            'fields': ('is_deleted',)
        }),
        ('일시', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
