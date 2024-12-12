from django.contrib import admin

from notifications.models import Task, Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("name", "contract_name", "subject", "content")
    search_fields = ("name", "contract_name", "subject")
    empty_value_display = "--empty--"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("template", "time_start", "started")
    search_fields = ("template", "started")
    empty_value_display = "--empty--"
