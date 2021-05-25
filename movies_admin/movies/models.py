import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

media_type = [
    ("film", _("фильм")),
    ("serial", _("сериал")),
]

person_type = [
    ("actor", _("актер")),
    ("writer", _("писатель")),
    ("director", _("режиссер")),
]


class AbstractUUID(models.Model):
    """Абстрактная модель для использования UUID в качестве PK."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Media(TimeStampedModel, AbstractUUID):
    """ Фильмы и сериалы """
    title = models.CharField(_("название"), max_length=255)
    description = models.TextField(_("описание"), blank=True, null=True)
    file_path = models.FileField(_("файл"), upload_to="film_works/", blank=True)
    creation_date = models.DateField(_("дата создания"), blank=True, null=True)
    certificate = models.TextField(_("сертификат"), blank=True, null=True)
    type = models.CharField(_("тип"), max_length=20, choices=media_type, blank=False)
    rating = models.FloatField(
        _("рейтинг"),
        validators=[MinValueValidator(0)],
        blank=True,
        default=0
    )

    # флаг индексации фильма, например для elasticsearch
    indexed = models.BooleanField(_("индексирован"), default=False)

    persons = models.ManyToManyField("Person", through="PersonMedia")
    genres = models.ManyToManyField("Genre", through="GenreMedia")

    class Meta:
        verbose_name = _("кинопроизведение")
        verbose_name_plural = _("кинопроизведения")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.indexed = False
        super(Media, self).save(*args, **kwargs)

    @staticmethod
    def take_indexed(medias):
        """" Снимает флаг индексации переданных фильмов """
        for media in medias:
            media.indexed = False
            media.save()


class Genre(AbstractUUID):
    """ Жанры """
    name = models.CharField(_("название"), max_length=255, unique=True)
    description = models.TextField(_("описание"), blank=True)

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")

    def save(self, *args, **kwargs):
        super(Genre, self).save(*args, **kwargs)
        Media.take_indexed([item.film for item in self.genremedia_set.all()])

    def __str__(self):
        return self.name


class Person(AbstractUUID):
    """ Люди """
    first_name = models.CharField(_("имя"), max_length=255)
    last_name = models.CharField(_("фамилия"), max_length=255)

    class Meta:
        verbose_name = _("персонаж")
        verbose_name_plural = _("персонаж")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        Media.take_indexed([item.film for item in self.personmedia_set.all()])


class GenreMedia(AbstractUUID):
    """ Жанры фильмов """
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("жанр фильма")
        verbose_name_plural = _("жанры фильмов")
        unique_together = [["genre", "film"]]

    def __str__(self):
        return f"{self.genre} {self.film}"


class PersonMedia(AbstractUUID):
    """ Люди в фильмах с их ролью """
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film = models.ForeignKey(Media, on_delete=models.CASCADE)
    person_type = models.CharField(_("роль"), max_length=20, choices=person_type, blank=False)

    class Meta:
        verbose_name = _("участник в создании фильма")
        verbose_name_plural = _("участики в создании фильма")
        unique_together = [["person", "film", "person_type"]]

    def __str__(self):
        return f"{self.person} {self.person_type} {self.film}"
