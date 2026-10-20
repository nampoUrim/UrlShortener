
from django.contrib import admin

from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    #defining columns displayed in the list
    list_display = (
        "short_code",
        "original_url",
        "created_at",
        "click_count",
    )
    #searching by short code ou original url
    search_fields = (
        "short_code",
        "original_url",
    )
    ordering = ("-created_at",)
