import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), default="", blank=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self) -> str:
        return self.name


class GenreFilmwork(UUIDMixin):  # noqa: DJ008
    film_work: models.ForeignKey["Filmwork"] = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre: models.ForeignKey[Genre] = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = 'content"."genre_film_work'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        unique_together = ["film_work", "genre"]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self) -> str:
        return self.full_name


class PersonFilmwork(UUIDMixin):  # noqa: DJ008
    class PesonFilmRole(models.TextChoices):
        ACTOR = "actor", _("actor")
        WRITER = "writer", _("writer")
        DIRECTOR = "director", _("director")

    film_work: models.ForeignKey["Filmwork"] = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person: models.ForeignKey[Person] = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_("role"), choices=PesonFilmRole.choices, default=PesonFilmRole.ACTOR)
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = 'content"."person_film_work'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        unique_together = ["film_work", "person", "role"]


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), default="", blank=True)
    creation_date = models.DateField(_("creation_date"), null=True, blank=True)
    file_path = models.FileField(_("file"), null=True, blank=True, upload_to="movies/media/filmwork/")
    rating = models.FloatField(
        _("rating"), null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(_("type"), choices=FilmType.choices, default=FilmType.MOVIE)
    genres = models.ManyToManyField(Genre, through=GenreFilmwork)
    persons = models.ManyToManyField(Person, through=PersonFilmwork)

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        db_table = 'content"."film_work'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")

    def __str__(self) -> str:
        return self.title
