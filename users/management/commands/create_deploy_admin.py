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
            user.email = email
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save(update_fields=(
                'email', 'is_active', 'is_staff', 'is_superuser', 'password',
            ))
            self.stdout.write(self.style.SUCCESS(f'Updated deployment admin {username!r}.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created deployment admin {username!r}.'))
