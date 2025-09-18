from django.views.generic import TemplateView
from wiki.models import Article

class HomeView(TemplateView):
    template_name = 'wiki/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.filter(status='PUBLISHED').order_by('-created_at')[:5]
        return context
    
from django.views.generic import View
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
import os

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