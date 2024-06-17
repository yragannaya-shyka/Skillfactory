from django import forms
from .models import Post
from datetime import date
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'topic', 'content']


    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")
        today  = date.today()
        post_limit = Post.objects.filter(author=author, public_date__date=today).count()
        if post_limit >=3:
            raise ValidationError("Нельзя публиковать больше трех постов в сутки!!!")
        return cleaned_data
