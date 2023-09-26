from django.urls import path,include
from tasks.views import RegistrationView,LoginView,TaskListView,TaskDetailView,TaskCreateView,TaskDeleteView,TaskUpdateView, MarkAsDoneView
from django.contrib.auth.views import LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

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
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='passwor_confirm_complete.html'), name='password_reset_complete'),
   
    #task crud views
    path('',TaskListView.as_view(),name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create-task/', TaskCreateView.as_view(), name='create_task'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('mark_as_done/<int:pk>/', MarkAsDoneView.as_view(), name='mark_as_done'),
    
    #rest api endpoints 
    path('api/', include(router.urls)),

    
]
