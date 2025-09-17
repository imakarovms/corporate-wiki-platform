from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('search/', views.ArticleSearchView.as_view(), name='article_search'),
    path('category/<slug:slug>/', views.ArticleListByCategoryView.as_view(), name='article_list_by_category'),

    # 👇 Сначала все "специальные" маршруты
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmarks'),
    path('bookmark/<slug:slug>/toggle/', views.BookmarkToggleView.as_view(), name='bookmark_toggle'),

    # 👇 Потом "общие" — <slug:slug> должен быть ПОСЛЕДНИМ
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
]