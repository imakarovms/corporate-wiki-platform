from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Invitation

@receiver(user_signed_up)
def mark_invitation_used(request, user, **kwargs):
    email = request.session.get('invite_email')
    if email:
        try:
            invite = Invitation.objects.get(email=email, is_used=False)
            invite.is_used = True
            invite.save()
        except Invitation.DoesNotExist:
            pass