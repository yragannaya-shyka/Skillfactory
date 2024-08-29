from django.db import models
from django.contrib.auth.models import AbstractUser
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name_category = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name_category


class Advertisement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    headline = models.CharField(max_length=100)
    text = RichTextUploadingField()
    some_datatime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.headline.title()}: {self.text[:20]}'

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


class Responses(models.Model):
    post = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)
    some_datatime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('advert_list')
