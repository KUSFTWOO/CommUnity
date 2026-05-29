from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('new/', views.create_view, name='create'),
    path('<int:pk>/respond/', views.respond_view, name='respond'),
    path('<int:pk>/results/', views.results_view, name='results'),
    path('<int:pk>/response/<int:response_pk>/', views.response_view, name='response_detail'),
    path('<int:pk>/delete/', views.delete_view, name='delete'),
]
