from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "Title",
        "CreateDate",
        "Is_active",
        "Completed",
        "EditeDate",
    )
    list_filter = ("CreateDate",)


# Register your models here.
