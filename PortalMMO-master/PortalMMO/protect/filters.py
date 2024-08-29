from django_filters import FilterSet
from myapp.models import Responses, Advertisement


class ResponsesFilters(FilterSet):


    class Meta:
        model = Responses
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(ResponsesFilters, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Advertisement.objects.filter(author=kwargs['request'])