from django.views.generic import TemplateView


   
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