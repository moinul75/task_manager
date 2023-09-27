from rest_framework import serializers
from .models import Task, TaskPhoto,User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )
        return user
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'completed', 'created_at', 'updated_at', 'user')

class TaskPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPhoto
        fields = ('id', 'photo', 'task')

class TaskWithPhotosSerializer(serializers.ModelSerializer):
    photos = TaskPhotoSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'completed', 'created_at', 'updated_at', 'user', 'photos')
        
        

