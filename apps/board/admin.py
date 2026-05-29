from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'views', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'content', 'author')
        }),
        ('통계', {
            'fields': ('views',)
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
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_reply', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('content', 'author', 'post', 'parent')
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
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__nickname', 'post__title']
    readonly_fields = ['created_at']
