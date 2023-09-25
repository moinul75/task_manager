from django.contrib import admin
from tasks.models import User,Task,TaskPhoto

class TaskPhotoInline(admin.StackedInline):
    model = TaskPhoto

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'priority', 'completed', 'created_at', 'updated_at']
    inlines = [TaskPhotoInline]
    




# Register your models here.
admin.site.register(User)
admin.site.register(Task, TaskAdmin)