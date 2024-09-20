from django.contrib import admin
from django.utils.html import mark_safe

from django.contrib import admin
from .models import Bouquet, Event, Budget, Consultation, Order


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

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone_number', 'registration_time', 'order_accepted')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone_number', 'address', 'order_time', 'bouquet',
                    'get_bouquet_price')
    search_fields = ('client_name', 'phone_number', 'address')
    list_filter = ('order_time', 'bouquet')
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('client_name', 'phone_number', 'address', 'order_time', 'bouquet')
        }),
    )

    def get_bouquet_price(self, obj):
        return obj.bouquet.price if obj.bouquet else "Нет букета"

    get_bouquet_price.short_description = "Цена букета"


admin.site.register(Bouquet, BouquetAdmin)
admin.site.register(Event)
admin.site.register(Budget)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Order, OrderAdmin)
