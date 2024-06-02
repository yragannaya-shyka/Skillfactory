from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view(), name='posts_search')
]
