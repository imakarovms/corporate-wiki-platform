from django.shortcuts import render

# Create your views here.
from allauth.account.views import SignupView
from .models import Invitation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

class InviteOnlySignupView(SignupView):
    template_name = 'users/invite_signup.html'

    def dispatch(self, request, *args, **kwargs):
        token = kwargs.get('token')
        invite = get_object_or_404(Invitation, token=token)
        if not invite.is_valid():
            return HttpResponse("Приглашение устарело или уже использовано.", status=400)
        # Передаём email в форму
        request.session['invite_email'] = invite.email
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'email': self.request.session.get('invite_email')}
        return kwargs

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'