from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth import authenticate,login
from django.contrib import messages

from tasks.models import User,Task,TaskPhoto
from .forms import UserRegistrationForm,LoginForm,TaskPhotoForm,TaskForm


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
    
    
#task list view 
class TaskListView(ListView):
    model = Task 
    template_name = 'task_list.html'  
    context_object_name = 'tasks' 
    ordering = ['-priority']  

    # You can override other attributes and methods as needed
    # For example, you can add filters or custom context data

    def get_queryset(self):
        # Customize the queryset if needed (e.g., filtering)
        queryset = super().get_queryset()  # Get the default queryset
        # Add your custom filtering or ordering logic here
        return queryset
    
#task details page 
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task' 



class TaskCreateView(CreateView):
    model = Task
    template_name = 'add_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = form.save()
        photo_form = TaskPhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            for photo in self.request.FILES.getlist('photo'):
                TaskPhoto.objects.create(task=task, photo=photo)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = TaskPhotoForm()
        return context