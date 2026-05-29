"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    # 앱 URL
    path("accounts/", include("apps.accounts.urls")),
    path("notices/", include("apps.notices.urls")),
    path("board/", include("apps.board.urls")),
    path("calendar/", include("apps.calendar_app.urls")),
    path("votes/", include("apps.votes.urls")),
    path("surveys/", include("apps.surveys.urls")),
    path("search/", include("apps.search.urls")),
    path("dashboard/", include("apps.dashboard.urls")),

    # Admin
    path("admin/", admin.site.urls),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
