from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post

class PostsList(ListView):
    model = Post
    ordering = "public_date"
    template_name = "posts.html"
    context_object_name = "posts"

class PostDetail(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
