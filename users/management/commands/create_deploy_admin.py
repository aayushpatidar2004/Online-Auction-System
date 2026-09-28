import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the initial deployment admin from environment variables, if configured.'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not all((username, email, password)):
            self.stdout.write('No deployment admin credentials configured; skipping.')
            return

        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user:
            self.stdout.write(f'Admin account {username!r} already exists; leaving it unchanged.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created deployment admin {username!r}.'))
