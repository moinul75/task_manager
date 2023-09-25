from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

class User(AbstractUser):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=100,unique=True)
    
    
    REQUIRED_FIELDS = ['fullname','username']
    
    USERNAME_FIELD = 'email'
        
    def __str__(self):
        return self.username 
    


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# adding  a model for task photos
class TaskPhoto(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='photos')
    photo =  models.FileField(upload_to='task_photos/')

    def __str__(self):
        return f"Photo for {self.task.title}"
