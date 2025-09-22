from django.shortcuts import redirect 
from django.urls import reverse
from django.conf import settings
import re

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Path: {request.path}")
        print(f"Authenticated: {request.user.is_authenticated}")
        
        # Разрешаем статические файлы
        if request.path.startswith(('/static/', '/media/')):
            print("Allowing static file")
            return self.get_response(request)
        
        # Разрешаем главную страницу и страницы аутентификации
        if request.path in ['/accounts/login/', '/accounts/signup/', '/accounts/logout/']:
            print("Allowing open URL")
            return self.get_response(request)
        
        # Разрешаем админку (но обычно там своя аутентификация)
        if request.path.startswith('/admin/'):
            print("Allowing admin URL")
            return self.get_response(request)
        
        # Проверяем аутентификацию
        if not request.user.is_authenticated:
            print("Redirecting to login")
            return redirect(f'/accounts/login/?next={request.path}')
        
        print("Allowing authenticated user")
        return self.get_response(request)