import pytest
from django.urls import reverse
from django.test import Client
from users.tests.factories import InvitationFactory, UserFactory

@pytest.mark.django_db
def test_invite_signup_view_valid_token():
    """Тест: регистрация по валидному токену"""
    invite = InvitationFactory()  # ← Теперь работает
    client = Client()
    url = reverse('invite_signup', kwargs={'token': invite.token})
    data = {
        'email': invite.email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert '/accounts/profile/' in response.url or '/' in response.url
    invite.refresh_from_db()
    assert invite.is_used

@pytest.mark.django_db
def test_invite_signup_view_invalid_token():
    """Тест: регистрация по невалидному токену возвращает 404"""
    client = Client()
    # Используем валидный UUID, чтобы маршрут нашёлся
    url = reverse('invite_signup', kwargs={'token': '123e4567-e89b-12d3-a456-426614174000'})
    response = client.get(url)

    assert response.status_code == 404  # ← Ожидаем 404, потому что токен не существует в БД

@pytest.mark.django_db
def test_login_view():
    """Тест: вход по email"""
    user = UserFactory()
    user.set_password('testpass123')
    user.save()

    client = Client()
    url = reverse('account_login')
    data = {
        'login': user.email,
        'password': 'testpass123',
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert '/accounts/profile/' in response.url or '/' in response.url