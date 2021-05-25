from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Media, Genre, Person, GenreMedia, PersonMedia


class Command(BaseCommand):
    help = "Deleting all data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting all data...")
        models = [Media, Genre, Person, PersonMedia, GenreMedia]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Done")
