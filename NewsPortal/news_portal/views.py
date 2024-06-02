from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class PostsList(ListView):
    model = Post
    ordering = "public_date"
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'news' in self.request.path_info:
            queryset = Post.objects.filter(post_type="NW")
        else:
            queryset = Post.objects.filter(post_type="AR")
        return queryset



class PostSearch(ListView):
    model = Post
    ordering = "public_date"
    template_name = "post_search.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        if 'news' in self.request.path_info:
            news = form.save(commit=False)
            news.post_type = Post.news
        return super().form_valid(form)



class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
