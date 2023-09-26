import django_filters
from .models import Task
from django import forms

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by title'}),
    )

    due_date = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='exact',  # Use 'exact' or 'iexact'
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    priority = django_filters.ModelChoiceFilter(
        field_name='priority',
        queryset=Task.objects.all(),  # Replace 'Priority' with your actual model name
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Priority',  # Label for the select field
    )
    completed = django_filters.BooleanFilter(
        field_name='completed',
        lookup_expr='exact',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Task
        fields = []
