from django.views.generic import TemplateView
from wiki.models import Article

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.filter(status='PUBLISHED').order_by('-created_at')[:5]
        return context