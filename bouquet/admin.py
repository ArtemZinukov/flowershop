from django.contrib import admin
from django.utils.html import mark_safe

from django.contrib import admin
from .models import Bouquet, Event, Budget


class BouquetAdmin(admin.ModelAdmin):
    list_display = ("title", "price",  "image_preview")
    search_fields = ("title", "composition")
    fields = ("title", "price",  "description", "composition",
              "image", "image_preview", "size", "events")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

    image_preview.short_description = "Image Preview"


admin.site.register(Bouquet, BouquetAdmin)
admin.site.register(Event)
admin.site.register(Budget)
