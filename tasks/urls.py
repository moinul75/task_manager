from django.urls import path,include
from tasks.views import RegistrationView,LoginView,TaskListView,TaskDetailView,TaskCreateView,TaskDeleteView,TaskUpdateView
from django.contrib.auth.views import LogoutView,PasswordResetView

#for rest api and router 
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    #for authentication
    path('register',RegistrationView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    #password reset 
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
   
    #task crud views
    path('',TaskListView.as_view(),name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create-task/', TaskCreateView.as_view(), name='create_task'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    
    #rest api endpoints 
    path('api/', include(router.urls)),

    
]
