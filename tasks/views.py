from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.views import APIView
from django.utils import timezone
from threading import Timer
import logging

logger = logging.getLogger(__name__)



class RegisterView(generics.CreateAPIView):
      serializer_class = UserSerializer
      permission_classes = [permissions.AllowAny]


class HealthCheckView(APIView):
      def get(self,request):
            return Response({"status":"ok"})
      


class TaskListCreateView(generics.ListCreateAPIView):
      serializer_class = TaskSerializer
      permission_classes = [permissions.IsAuthenticated]


      def get_queryset(self):
          queryset = Task.objects.filter(user=self.request.user)
          status_param = self.request.query_params.get("status")
          if status_param:
            queryset = queryset.filter(status=status_param)

          return queryset


      def perform_create(self, serializer):
          task = serializer.save(user=self.request.user)
          logger.info(f"Task craeted: {task.name} by user {self.request.user}")

          def complete_task():
               task.status = "completed"
               task.save()
               logger.info(f"Task completed : {task.name}")

          Timer(5.0, complete_task).start()     


class TaskDeleteView(generics.DestroyAPIView):    
      queryset = Task.objects.all()
      serializer_class = TaskSerializer
      permission_classes = [permissions.IsAuthenticated]


      def get_queryset(self):
           return Task.objects.filter(user=self.request.user)
