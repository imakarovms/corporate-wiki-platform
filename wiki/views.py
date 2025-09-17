from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Category, Bookmark, ViewHistory
from django.urls import reverse_lazy, reverse
from .forms import ArticleForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='PUBLISHED').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None)  # Только корневые категории
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Хлебные крошки: Главная → Категория → Статья
        article = self.get_object()
        context['breadcrumbs'] = [
            {'name': 'Главная', 'url': reverse('home')},
            {'name': article.category.name, 'url': reverse('wiki:article_list_by_category', kwargs={'slug': article.category.slug})},
            {'name': article.title, 'url': ''},
        ]
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            ViewHistory.objects.get_or_create(
                user=request.user,
                article=self.get_object()
            )
        return response

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'
    success_url = reverse_lazy('wiki:article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'PENDING'
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return self.object.get_absolute_url()
    

class ArticleSearchView(ListView):
    model = Article
    template_name = 'wiki/article_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                status='PUBLISHED'
            ).annotate(
                search=SearchVector('title', 'content')
            ).filter(search=query)
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context    
    
class ArticleListByCategoryView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        return Article.objects.filter(
            status='PUBLISHED',
            category__in=category.get_descendants(include_self=True)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context    
    
class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'wiki/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

class BookmarkToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            article=article
        )
        if not created:
            bookmark.delete()
            is_bookmarked = False
        else:
            is_bookmarked = True
        return JsonResponse({'is_bookmarked': is_bookmarked})

class ViewHistoryListView(LoginRequiredMixin, ListView):
    model = ViewHistory
    template_name = 'wiki/history.html'
    context_object_name = 'history'
    paginate_by = 20
