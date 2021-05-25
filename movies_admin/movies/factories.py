import factory
from factory.django import DjangoModelFactory
from .models import Media, Genre, Person, PersonMedia


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: 'genre{}'.format(n))


class MediaFactory(DjangoModelFactory):
    class Meta:
        model = Media

    title = factory.Faker("name")
    description = factory.Faker("sentence", nb_words=64, variable_nb_words=True)
    creation_date = factory.Faker("date")
    rating = factory.Faker("random_number", digits=2)


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class PersonMediaFactory(DjangoModelFactory):
    class Meta:
        model = PersonMedia
