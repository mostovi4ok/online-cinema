# Generated by Django 4.2.11 on 2024-06-19 16:40

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL("CREATE SCHEMA IF NOT EXISTS content"),
        migrations.CreateModel(
            name="Filmwork",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("modified", models.DateTimeField(auto_now=True, verbose_name="Изменено")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("description", models.TextField(blank=True, null=True, verbose_name="description")),
                ("creation_date", models.DateField(null=True, verbose_name="creation_date")),
                (
                    "rating",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("movie", "movie"), ("tv_show", "tv_show")], default="movie", verbose_name="type"
                    ),
                ),
            ],
            options={
                "verbose_name": "Filmwork",
                "verbose_name_plural": "Filmworks",
                "db_table": 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("modified", models.DateTimeField(auto_now=True, verbose_name="Изменено")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("description", models.TextField(blank=True, null=True, verbose_name="description")),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
                "db_table": 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("modified", models.DateTimeField(auto_now=True, verbose_name="Изменено")),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255, verbose_name="full_name")),
            ],
            options={
                "verbose_name": "Person",
                "verbose_name_plural": "Persons",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmwork",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("role", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("film_work", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.filmwork")),
                ("person", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.person")),
            ],
            options={
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmwork",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("film_work", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.filmwork")),
                ("genre", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.genre")),
            ],
            options={
                "db_table": 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genres",
            field=models.ManyToManyField(through="movies.GenreFilmwork", to="movies.genre"),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="persons",
            field=models.ManyToManyField(through="movies.PersonFilmwork", to="movies.person"),
        ),
    ]
