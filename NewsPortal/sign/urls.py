from django.urls import path
from .views import IndexView, make_me_author
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', IndexView.as_view()),
    path('sign/make-me-author/', make_me_author, name = 'make_me_author'),
    path('logout/', LogoutView.as_view(template_name ='posts.html'), name='logout'),
]
