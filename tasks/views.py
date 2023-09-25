from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth import authenticate,login
from django.contrib import messages

from tasks.models import User,Task,TaskPhoto
from .forms import UserRegistrationForm,LoginForm


class RegistrationView(View):
    form_class = UserRegistrationForm  
    
    def get(self, request):
        
        if request.user.is_authenticated: 
            return redirect('task_list')
        
        form = self.form_class()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login') 
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated: 
            return redirect('task_list')
        
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Log in Successfully')
                return redirect('task_list') 
            else:
                form.add_error('email', 'Invalid email or password')

        return render(request, self.template_name, {'form': form})
    
    
#logout view 



