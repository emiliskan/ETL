from django.core.management.base import BaseCommand
import os
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crate a superuser, and allow password to be provided'

    def handle(self, *args, **options):
        password = os.getenv('SUPERUSER_PASS')
        username = os.getenv('SUPERUSER_NAME')
        if User.objects.filter(username=username).exists():
            return

        User.objects.create_superuser(username, 'admin@example.com', password)
