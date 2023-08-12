from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .filters import NewsFilter
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import Post, Category
from pprint import pprint
from .forms import PostForm
from django.urls import reverse_lazy

from django.shortcuts import redirect, render, get_object_or_404


@login_required
def upgrade_me(request):
    user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(user)
    return redirect('profile')

def profile(request):
    context = {'is_not_author': not request.user.groups.filter(name='authors').exists()}
    return render(request, 'profile.html', context)

class PostList(ListView, LoginRequiredMixin):
    model = Post
    ordering = 'post_header'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class Event(DetailView):
    model = Post
    template_name = 'event.html'
    context_object_name = 'event'


class NewsSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    ordering = ['-post_time_in']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        pprint(context)
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post', )
    login_url = '/accounts/login/'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.post_link = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_link=self.post_link).order_by('-post_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_link.subscribers.all()
        context['is_subscriber'] = self.request.user in self.post_link.subscribers.all()
        context['post_link'] = self.post_link
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You subscribed to the category: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'You unsubscribed from category: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})
