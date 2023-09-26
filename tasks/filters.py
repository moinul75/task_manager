import django_filters
from .models import Task
from django import forms

PRIORITY_CHOICES = (
    (1, 'High'),
    (2, 'Medium'),
    (3, 'Low'),
)

class TaskFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date',  
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )


    due_date = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='exact', 
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    priority = django_filters.ChoiceFilter(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Priority',
    )
    completed = django_filters.BooleanFilter(
        field_name='completed',
        lookup_expr='exact',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Task
        fields = []
