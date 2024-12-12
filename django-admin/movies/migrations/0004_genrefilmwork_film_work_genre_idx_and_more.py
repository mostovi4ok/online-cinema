# Generated by Django 4.2.11 on 2024-06-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_alter_genrefilmwork_options_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="genrefilmwork",
            constraint=models.UniqueConstraint(fields=("film_work_id", "genre_id"), name="film_work_genre_idx"),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work_id", "person_id", "role"), name="film_work_person_role_idx"
            ),
        ),
    ]
