

from django.urls import path
from .views import RegisterView, TaskListCreateView, TaskDeleteView, HealthCheckView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
