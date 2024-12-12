from django.db import models


class Template(models.Model):
    name = models.CharField("Название", max_length=255)
    contract_name = models.CharField("Название схемы", max_length=255)
    subject = models.CharField("Заголовок", max_length=255)
    content = models.TextField("Текст")

    class Meta:
        db_table = "templates"
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    name = models.CharField("Название", max_length=255)
    template: models.ForeignKey["Template"] = models.ForeignKey("Template", on_delete=models.CASCADE)
    time_start = models.DateTimeField("Время запуска")
    started = models.BooleanField("Запущен", default=False)

    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self) -> str:
        return self.name
