from typing import Any, LiteralString

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("name", "description", "created", "modified")
    search_fields = ("id", "name", "description")
    empty_value_display = "--empty--"


class GenreFilmworkInline(admin.TabularInline):  # pyright: ignore[reportMissingTypeArgument]
    model = GenreFilmwork
    autocomplete_fields = ("genre",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("full_name", "created", "modified")
    search_fields = ("id", "full_name")
    empty_value_display = "--empty--"


class PersonFilmworkInline(admin.TabularInline):  # pyright: ignore[reportMissingTypeArgument]
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    inlines = (PersonFilmworkInline, GenreFilmworkInline)
    list_display = ("title", "type", "creation_date", "rating", "created", "modified", "get_genres", "get_persons")
    list_filter = ("type", "creation_date", "genres")
    search_fields = ("id", "title", "description", "persons__full_name")
    date_hierarchy = "creation_date"
    empty_value_display = "--empty--"
    list_prefetch_related = ("genres", "persons")

    def get_queryset(self, request: HttpRequest) -> QuerySet:  # pyright: ignore
        return super().get_queryset(request).prefetch_related(*self.list_prefetch_related)  # pyright: ignore[reportUnknownVariableType]

    def get_genres(self, obj: Any) -> LiteralString:
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _("Genres")  # pyright: ignore[reportFunctionMemberAccess]

    def get_persons(self, obj: Any) -> LiteralString:
        return ", ".join([person.full_name for person in obj.persons.all()])

    get_persons.short_description = _("Persons")  # pyright: ignore[reportFunctionMemberAccess]
