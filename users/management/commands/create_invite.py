from django.core.management.base import BaseCommand
from users.models import Invitation

class Command(BaseCommand):
    help = 'Create an invitation for a given email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        invite, created = Invitation.objects.get_or_create(email=email, defaults={'is_used': False})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Invite created: {invite.token}'))
        else:
            self.stdout.write(self.style.WARNING('Invite already exists'))