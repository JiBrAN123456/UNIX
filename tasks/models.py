from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager
from django.conf import settings

'''
class UserManager(BaseUserManager):
    
    def createUser(self, email, password= None,**extra_fields ):
        if not email:
            raise ValueError("Email Required")
        
        email = self.normalize(email)
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superUser(self, email , password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",True)

        return self.createUser(email, password, **extra_fields)
'''


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

    def __str__(self):
        return f"{self.name} ({self.status})"