from django.urls import path
from .views import PostsList, PostDetail, PostSearch, NewsCreate, NewsUpdate, NewsDelete, CategoryListView, subscribe, IndexView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    path('categories/<int:pk>', cache_page(60*5)(CategoryListView.as_view()), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('tasks/', IndexView.as_view())
]
