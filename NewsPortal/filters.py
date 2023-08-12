from django_filters import FilterSet, CharFilter, DateFilter, DateTimeFilter, ModelChoiceFilter
from .models import Post, Author
from django import forms


class NewsFilter(FilterSet):
    post_header = CharFilter(lookup_expr='icontains', label='По заголовку')
    post_author = ModelChoiceFilter(lookup_expr='exact', label='По имени автора', queryset=Author.objects.all())
    post_time_in = DateFilter(field_name='post_time_in', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}), label='Позже чем')

    class Meta:
        model = Post
        fields = ['post_header', 'post_author', 'post_time_in']
