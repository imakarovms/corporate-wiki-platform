from django.shortcuts import render
import os
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Category, Bookmark, ViewHistory
from django.urls import reverse_lazy, reverse
from .forms import ArticleForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse  # ← ДОБАВЬТЕ HttpResponse
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string  # ← ДОБАВЬТЕ render_to_string
from django.middleware.csrf import get_token  # ← ДОБАВЬТЕ get_token для CSRF

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(status='PUBLISHED').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None)
        
        # Добавляем информацию о закладках для каждой статьи
        if self.request.user.is_authenticated:
            # Получаем ID статей, которые находятся в закладках у пользователя
            bookmarked_article_ids = Bookmark.objects.filter(
                user=self.request.user
            ).values_list('article_id', flat=True)
            context['bookmarked_article_ids'] = list(bookmarked_article_ids)
        else:
            context['bookmarked_article_ids'] = []
            
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        # Проверяем, добавлена ли статья в закладки
        is_bookmarked = False
        if self.request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(
                user=self.request.user, 
                article=article
            ).exists()
        
        context['is_bookmarked'] = is_bookmarked
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
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.filter(parent=None)
        
        # Добавляем информацию о закладках
        if self.request.user.is_authenticated:
            bookmarked_article_ids = Bookmark.objects.filter(
                user=self.request.user
            ).values_list('article_id', flat=True)
            context['bookmarked_article_ids'] = list(bookmarked_article_ids)
        else:
            context['bookmarked_article_ids'] = []
            
        return context
    
class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = 'wiki/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by('-created_at')  # ← Добавьте ordering

class BookmarkToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        source_page = request.POST.get('source_page', 'article_detail')
        
        # Проверяем существование закладки
        bookmark_exists = Bookmark.objects.filter(
            user=request.user,
            article=article
        ).exists()
        
        if bookmark_exists:
            # Удаляем закладку
            Bookmark.objects.filter(user=request.user, article=article).delete()
            is_bookmarked = False
        else:
            # Создаем закладку
            Bookmark.objects.create(user=request.user, article=article)
            is_bookmarked = True
        
        # Обработка для разных страниц
        if source_page == 'bookmarks' and not is_bookmarked:
            # Удаление со страницы закладок - возвращаем пустой HTML
            return HttpResponse('')
        
        elif source_page == 'article_list':
            # Для списка статей
            if is_bookmarked:
                button_html = '''
                <button type="submit" class="btn btn-warning btn-sm">
                    <i class="fas fa-bookmark"></i> Удалить из закладок
                </button>
                '''
            else:
                button_html = '''
                <button type="submit" class="btn btn-outline-warning btn-sm">
                    <i class="far fa-bookmark"></i> Добавить в закладки
                </button>
                '''
            
            html = f'''
            <form method="post" 
                  action="{reverse('wiki:bookmark_toggle', args=[article.slug])}" 
                  hx-post="{reverse('wiki:bookmark_toggle', args=[article.slug])}"
                  hx-target="#bookmark-button-{article.slug}"
                  hx-swap="outerHTML"
                  class="d-inline">
                <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
                <input type="hidden" name="source_page" value="article_list">
                {button_html}
            </form>
            '''
            return HttpResponse(html)
        
        else:
            # Для детальной страницы статьи
            if is_bookmarked:
                button_html = '''
                <button type="submit" class="btn btn-warning btn-sm">
                    <i class="fas fa-bookmark"></i> Удалить из закладок
                </button>
                '''
            else:
                button_html = '''
                <button type="submit" class="btn btn-outline-warning btn-sm">
                    <i class="far fa-bookmark"></i> Добавить в закладки
                </button>
                '''
            
            html = f'''
            <form method="post" 
                  action="{reverse('wiki:bookmark_toggle', args=[article.slug])}" 
                  hx-post="{reverse('wiki:bookmark_toggle', args=[article.slug])}"
                  hx-target="this"
                  hx-swap="outerHTML"
                  class="d-inline">
                <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
                <input type="hidden" name="source_page" value="article_detail">
                {button_html}
            </form>
            '''
            return HttpResponse(html)

class ViewHistoryListView(LoginRequiredMixin, ListView):
    model = ViewHistory
    template_name = 'wiki/history.html'
    context_object_name = 'history'
    paginate_by = 20


class UploadFileView(View):
    def post(self, request):
        if 'upload' in request.FILES:
            file = request.FILES['upload']
            filename = file.name
            filepath = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            url = f"{settings.MEDIA_URL}uploads/{filename}"
            return JsonResponse({
                'uploaded': 1,
                'fileName': filename,
                'url': url
            })
        
        return JsonResponse({'uploaded': 0, 'error': {'message': 'Failed to upload file'}}, status=400)