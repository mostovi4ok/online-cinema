# Generated by Django 4.2.11 on 2024-11-08 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Template",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("contract_name", models.CharField(max_length=255, verbose_name="Название схемы")),
                ("subject", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("content", models.TextField(verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Шаблон",
                "verbose_name_plural": "Шаблоны",
                "db_table": "templates",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("time_start", models.DateTimeField(verbose_name="Время запуска")),
                ("started", models.BooleanField(default=False, verbose_name="Запущен")),
                (
                    "template",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="notifications.template"),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "db_table": "tasks",
            },
        ),
    ]
