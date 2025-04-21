from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class User(AbstractUser):
    pass


class Task(models.Model):
    STATUS_CHOICES = [("running","Running"),
                      ('completed',"Completed"),
                      ('failed',"Failed")]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, default= "running")
    created_at = models.DateTimeField(auto_now_add=True)

    