from django.db import models
from django.contrib.auth.models import User


PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# adding  a model for task photos
class TaskPhoto(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='task_photos/') 

    def __str__(self):
        return f"Photo for {self.task.title}"
