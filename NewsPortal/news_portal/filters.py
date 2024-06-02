from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    public_date = DateTimeFilter(widget=forms.DateInput(attrs={'type': 'date'}), field_name='public_date', lookup_expr='gt')
    class Meta:
        model = Post
        fields = {
            'topic':['icontains'],
            'author' :['exact'],

        }
