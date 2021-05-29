from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Media, Genre, Person, GenreMedia, PersonMedia
from movies.factories import MediaFactory, GenreFactory
import random

from movies.factories import PersonFactory

"""
NUM_FILM = 1000000000
NUM_SERIAL = 2000000
NUM_MEDIA = NUM_FILM + NUM_SERIAL
NUM_GENRE = 10000
NUM_PERSONS = 1000

"""
# for test:
NUM_FILM = 1000
NUM_SERIAL = 200
NUM_MEDIA = NUM_FILM + NUM_SERIAL
NUM_GENRE = 100
NUM_PERSONS = 100


class Command(BaseCommand):
    help = "Generate test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("deleting old data")
        models = [Media, Genre, Person, PersonMedia, GenreMedia]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("generating new data...")

        self.stdout.write("genres")
        genres = []
        for _ in range(NUM_GENRE):
            genres.append(GenreFactory())

        self.stdout.write("persons")
        persons = []
        for _ in range(NUM_PERSONS):
            persons.append(PersonFactory())

        self.stdout.write("films")
        for _ in range(NUM_MEDIA):
            # рандомно сгенирируем количество жанров и участников фильма
            # но чтоб их не было больше 3
            random_genres = random.sample(genres, random.randint(1, 3))
            random_persons = random.sample(persons, random.randint(1, 3))

            film = MediaFactory()
            film.genres.set(random_genres)
            film.persons.set(random_persons)

        self.stdout.write("done")
