from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'file']
        