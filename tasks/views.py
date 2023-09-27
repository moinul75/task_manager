from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import TaskFilter
from tasks.models import User,Task,TaskPhoto
from .forms import UserRegistrationForm,LoginForm,TaskPhotoForm,TaskForm,TaskPhotoFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework import viewsets, pagination
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import  TaskSerializer,TaskPhotoSerializer,TaskWithPhotosSerializer,UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token




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
           
            task = Task.objects.get(pk=pk)
            
           
            messages.success(request, 'Task deleted successfully')
            
          
            task.delete()
            
    
            return JsonResponse({'message': 'Task deleted successfully'})
        
        except Task.DoesNotExist:
           
            messages.error(request, 'Task not found')
            return JsonResponse({'error': 'Task not found'}, status=404)

#updated task view 
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'update_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        task = form.save()

       
        photo_form = TaskPhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            for photo in self.request.FILES.getlist('photo'):
                TaskPhoto.objects.create(task=task, photo=photo)

        existing_photos = TaskPhoto.objects.filter(task=task)
        formset = TaskPhotoFormSet(self.request.POST, self.request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.task = task
                instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Create or retrieve the user's token
            return Response({'user_id': user.id, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)  # Create or retrieve the user's token
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.auth.delete() 
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
class CustomPageNumberPagination(LoginRequiredMixin,pagination.PageNumberPagination):
    page_size = 2  
    page_size_query_param = 'page_size'
    max_page_size = 50

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskWithPhotosSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        task_serializer = TaskSerializer(data=request.data)
        
        if task_serializer.is_valid():
            task = task_serializer.save(user=request.user)
            photos_data = request.FILES.getlist('photos[]')
            print(photos_data)
            photo_serializer = TaskPhotoSerializer(data=photos_data, many=True)
            print(photo_serializer)
            if photo_serializer.is_valid():
                for photo_data in photos_data:
                    photo_serializer.save(task=task)
                
                return Response(task_serializer.data, status=status.HTTP_201_CREATED)
            else:
                task.delete()
                return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        task_serializer = TaskSerializer(instance, data=request.data, partial=True)
        if task_serializer.is_valid():
            task_serializer.save()

            # Update associated TaskPhoto instances
            photo_data = request.data.get('photos', [])
            for photo_item in photo_data:
                photo_id = photo_item.get('id')
                if photo_id:
                    try:
                        task_photo = TaskPhoto.objects.get(id=photo_id)
                        task_photo_serializer = TaskPhotoSerializer(task_photo, data=photo_item, partial=True)
                        if task_photo_serializer.is_valid():
                            task_photo_serializer.save()
                        else:
                            return Response(task_photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    except TaskPhoto.DoesNotExist:
                        pass
                else:
                    task_photo_serializer = TaskPhotoSerializer(data=photo_item)
                    if task_photo_serializer.is_valid():
                        task_photo_serializer.save(task=instance)
                    else:
                        return Response(task_photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(task_serializer.data, status=status.HTTP_200_OK)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Deleted data successfully'},status=status.HTTP_204_NO_CONTENT)

    
    










 
 
 