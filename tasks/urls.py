from django.urls import path 
from tasks.views import RegistrationView,LoginView,TaskListView
from django.contrib.auth.views import LogoutView,PasswordResetView


urlpatterns = [
    path('register',RegistrationView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
   
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
]
