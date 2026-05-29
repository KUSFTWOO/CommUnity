from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # 메인 대시보드
    path('', views.index, name='index'),

    # 회원 관리
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),

    # 공지사항 관리
    path('notices/', views.notices, name='notices'),
    path('notices/<int:notice_id>/', views.notice_manage, name='notice_manage'),

    # 게시글 관리
    path('posts/', views.posts, name='posts'),
    path('posts/<int:post_id>/', views.post_manage, name='post_manage'),

    # 일정 관리
    path('calendar/', views.calendar_manage, name='calendar_manage'),
    path('calendar/<int:event_id>/', views.event_manage, name='event_manage'),

    # 투표 관리
    path('polls/', views.polls, name='polls'),
    path('polls/<int:poll_id>/', views.poll_detail, name='poll_detail'),

    # 설문조사 관리
    path('surveys/', views.surveys, name='surveys'),
    path('surveys/<int:survey_id>/', views.survey_detail, name='survey_detail'),

    # 신고 처리
    path('reports/', views.reports, name='reports'),
]
