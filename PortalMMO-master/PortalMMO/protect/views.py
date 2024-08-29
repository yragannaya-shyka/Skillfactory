from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.models import Advertisement, Responses
from protect.filters import ResponsesFilters


class IndexView(LoginRequiredMixin, ListView):
    model = Responses
    template_name = 'protect/index.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = Responses.objects.filter(post__author=self.request.user.id)
        self.filterset = ResponsesFilters(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Responses.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not Advertisement.objects.filter(author=self.request.user).exists()
        context['filterset'] = self.filterset
        return context