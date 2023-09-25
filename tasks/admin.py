from django.contrib import admin
from tasks.models import User,Task,TaskPhoto

class TaskPhotoInline(admin.StackedInline):
    model = TaskPhoto

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'priority', 'completed', 'created_at', 'updated_at']
    inlines = [TaskPhotoInline]
    

#User view > email username last logging superuser updatedat 
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_superuser', 'last_login', 'date_joined', 'date_joined']
    list_display_links = ['email']




# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Task, TaskAdmin)