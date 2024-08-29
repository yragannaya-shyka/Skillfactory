from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import AdvertisementFilter
from .forms import PostForm, ResponseForm
from .models import Advertisement, Responses, User, Category
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, template_name='invalid_code.html')
        return redirect('account_login')


class AdvertisementList(ListView):
    model = Advertisement
    ordering = '-some_datatime'
    template_name = 'flatpages/Advertisement.html'
    context_object_name = 'advertisement'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'flatpages/detail.html'
    context_object_name = 'detail'


class PostSearch(ListView):
    model = Advertisement
    ordering = '-some_datatime'
    template_name = 'flatpages/search.html'
    context_object_name = 'posts_search'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertisementFilter(self.request.GET, queryset)
        if self.request.GET:
            return self.filterset.qs
        return Advertisement.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdvertisementCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Advertisement
    template_name = 'flatpages/post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.username
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = PostForm
    template_name = 'flatpages/post_create.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Advertisement.objects.get(pk=self.kwargs.get('pk')).author
        return context


class AdvertisementDelete(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('advert_list')

class ResponsesCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Responses
    template_name = 'flatpages/response_create.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.user = self.request.user
        response.post_id = self.kwargs['pk']
        response.save()
        return super().form_valid(form)

def accept_response(request, responses_id):
    response = get_object_or_404(Responses, pk=responses_id)
    response.status = True
    response.save()
    return redirect(reverse('advert_list'))

def delete_response(request, responses_id):
    response = get_object_or_404(Responses, pk=responses_id)
    response.delete()
    return redirect(reverse('advert_list'))


class CategoryListView(LoginRequiredMixin, AdvertisementList):
    model = Advertisement
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Advertisement.objects.filter(category=self.category).order_by('-some_datatime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})
