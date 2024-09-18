from django.contrib import admin
from django.utils.html import mark_safe

from django.contrib import admin
from .models import Bouquet, Event


class BouquetAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "status", "image_preview")
    list_filter = ("status",)
    search_fields = ("title", "composition_description")
    fields = ("title", "price", "status", "composition_description",
              "image", "image_preview", "size_description", "events")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

    image_preview.short_description = "Image Preview"


admin.site.register(Bouquet, BouquetAdmin)
admin.site.register(Event)
