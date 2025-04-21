# tasks/urls.py

from django.urls import path
from .views import RegisterView, TaskListCreateView, TaskDeleteView, HealthCheckView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDeleteView.as_view()),
    path('health/', HealthCheckView.as_view()),
]
