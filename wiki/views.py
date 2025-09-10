from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Category
from django.urls import reverse_lazy
from .forms import ArticleForm

class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='PUBLISHED').order_by('-created_at')

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

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