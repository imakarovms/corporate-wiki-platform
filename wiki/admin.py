from django.contrib import admin

# Register your models here.
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Tag, Article

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'author', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    actions = ['approve_articles', 'reject_articles']

    def approve_articles(self, request, queryset):
        queryset.update(status='PUBLISHED')
        self.message_user(request, f"Опубликовано {queryset.count()} статей.")
    approve_articles.short_description = "✅ Опубликовать"

    def reject_articles(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, f"Отклонено {queryset.count()} статей.")
    reject_articles.short_description = "❌ Отклонить"