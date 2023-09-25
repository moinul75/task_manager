from django import forms 
from .models import Task,TaskPhoto ,User 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from multiupload.fields import MultiFileField


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'username', 'password']  # Include the fields you want

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=255,
        help_text='Please enter a valid email address.'
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        help_text='Your username should be unique.'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        max_length=128,
        help_text='Password should be at least 8 characters long.'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        existing_user = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise forms.ValidationError('This username is already taken.')
        return username 
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=255,
        help_text='Please enter a valid email address.'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        max_length=128,
        help_text='Password should be at least 8 characters long.'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None and not user.check_password(password):
                # Add a password error to the password field
                self.add_error('password', 'The provided password is incorrect.')

# #adding task forms 
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed']



class TaskPhotoForm(forms.ModelForm):
    class Meta:
        model = TaskPhoto
        fields = ['photo']
  # Use MultiValueField with MultipleHiddenInput widget for multiple file uploads
    # photo = forms.FileField(
    #     widget=forms.ClearableFileInput(),
    # )
    photo = MultiFileField(
        min_num=1,
        max_num=10,  # Adjust the maximum number of files if needed
        max_file_size=1024 * 1024 * 5,  # 5 MB
    )