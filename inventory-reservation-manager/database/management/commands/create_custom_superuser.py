from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a custom superuser if one doesn\'t already exist.'

    def add_arguments(self, parser):
        # Add command line arguments for username, email, and password
        parser.add_argument('username', type=str, help='Username for the superuser')
        parser.add_argument('email', type=str, help='Email for the superuser')
        parser.add_argument('password', type=str, help='Password for the superuser')

    def handle(self, *args, **kwargs):
        # Get the arguments
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        # Check if a superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING(f'Superuser already exists.'))
        else:
            # Create the superuser
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
