from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import TaskFilter
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import TaskWithPhotosSerializer

from tasks.models import User,Task,TaskPhoto
from .forms import UserRegistrationForm,LoginForm,TaskPhotoForm,TaskForm,TaskPhotoFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q



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
    
    


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    ordering = ['priority']
    paginate_by = 2
    filterset_class = TaskFilter

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current page number from the request
        page_number = self.request.GET.get('page')
        
        # Create a paginator for the queryset
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        
        # Get the current page
        page = paginator.get_page(page_number)
        
        context['tasks'] = page
        context['search_form'] = TaskFilter(data=self.request.GET, queryset=self.get_queryset())
        
        return context
    
#task details page 
class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task' 


class TaskCreateView(LoginRequiredMixin,CreateView):
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
        messages.success(self.request, 'Task added successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = TaskPhotoForm()
        return context 
    def get_success_url(self) -> str:
        return reverse_lazy('task_list')
    




#tasks delete 
class TaskDeleteView(LoginRequiredMixin,View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            # Get the task by primary key (pk)
            task = Task.objects.get(pk=pk)
            
            # Send a success message before deletion
            messages.success(request, 'Task deleted successfully')
            
            # Delete the task
            task.delete()
            
            # Return a JSON response indicating success
            return JsonResponse({'message': 'Task deleted successfully'})
        
        except Task.DoesNotExist:
            # Send an error message and a JSON response with a 404 status code
            messages.error(request, 'Task not found')
            return JsonResponse({'error': 'Task not found'}, status=404)

#updated task view 
class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'update_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = form.save()

        # Handle updating existing photos
        photo_form = TaskPhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            for photo in self.request.FILES.getlist('photo'):
                TaskPhoto.objects.create(task=task, photo=photo)

        # Handle retaining previously uploaded photos
        existing_photos = TaskPhoto.objects.filter(task=task)
        formset = TaskPhotoFormSet(self.request.POST, self.request.FILES, instance=task)
        if formset.is_valid():
            formset.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = TaskPhotoForm()
        task = self.get_object()
        context['existing_photos'] = TaskPhoto.objects.filter(task=task)
        return context

    def get_success_url(self):
        return reverse_lazy('task_list')


#mark as done 
class MarkAsDoneView(LoginRequiredMixin,View):
    def post(self,request,pk):
        task = get_object_or_404(Task, id=pk)
        print(task)
        task.completed = True
        task.save()
        return redirect('task_list')


#REST API using viewset (CRUD)

class TaskViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskWithPhotosSerializer
    
    
    










 
 
 