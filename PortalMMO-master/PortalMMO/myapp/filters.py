from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, DateFilter
from .models import User
from django import forms


class AdvertisementFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author', queryset=User.objects.all(), label='автор')
    headline = CharFilter(field_name='headline', lookup_expr='contains', label='заголовок')
    some_datatime = DateFilter(
        field_name='some_datatime',
        lookup_expr='gte',  # lookup_expr='lt',
        label='дата добавления',
        widget=forms.DateInput(attrs={'type': 'date'})
    )