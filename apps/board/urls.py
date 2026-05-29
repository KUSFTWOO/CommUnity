from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('new/', views.create_view, name='create'),
    path('<int:pk>/', views.detail_view, name='detail'),
    path('<int:pk>/delete/', views.delete_view, name='delete'),
    path('<int:pk>/comment/', views.comment_create_view, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
    path('<int:pk>/like/', views.like_toggle_view, name='like_toggle'),
]
