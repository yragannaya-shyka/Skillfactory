from django.urls import path
from .views import AdvertisementList, AdvertisementDetail, PostSearch, AdvertisementCreate, AdvertisementUpdate, \
    AdvertisementDelete, ResponsesCreate, accept_response, delete_response, ConfirmUser, CategoryListView, subscribe

urlpatterns = [
    path('posts/', AdvertisementList.as_view(), name='advert_list'),
    path('detail/<int:pk>', AdvertisementDetail.as_view(), name='detail'),
    path('posts/search/', PostSearch.as_view(), name='search'),
    path('posts/create/', AdvertisementCreate.as_view(), name='create'),
    path('posts/<int:pk>/update/', AdvertisementUpdate.as_view(), name='update'),
    path('posts/<int:pk>/delete/', AdvertisementDelete.as_view(), name='delete'),
    path('<int:pk>/response/create/', ResponsesCreate.as_view(), name='response_create'),
    path('accept_replay/<int:responses_id>', accept_response, name='accept_response'),
    path('delete_replay/<int:responses_id>', delete_response, name='delete_response'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),

    path('posts/categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('posts/categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
