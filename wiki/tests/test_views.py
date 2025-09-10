import pytest
from django.urls import reverse
from django.test import Client
from .factories import ArticleFactory, UserFactory

@pytest.mark.django_db
def test_article_list_view():
    article = ArticleFactory()
    client = Client()
    response = client.get(reverse('wiki:article_list'))
    assert response.status_code == 200
    assert article.title in str(response.content)

@pytest.mark.django_db
def test_article_detail_view():
    article = ArticleFactory()
    client = Client()
    url = reverse('wiki:article_detail', kwargs={'slug': article.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert article.title in str(response.content)

@pytest.mark.django_db
def test_article_create_view_requires_login():
    client = Client()
    url = reverse('wiki:article_create')
    response = client.get(url)
    assert response.status_code == 302
    assert '/accounts/login/' in response.url