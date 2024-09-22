import asyncio
from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib import admin
from django.conf import settings
from aiogram import Bot
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
    list_display = ('client_name', 'phone_number',
                    'registration_time', 'order_accepted')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone_number', 'address', 'order_time', 'bouquet',
                    'get_bouquet_price', 'status')
    search_fields = ('client_name', 'phone_number', 'address')
    list_filter = ('order_time', 'bouquet')
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('client_name', 'phone_number', 'address', 'order_time', 'bouquet', 'status')
        }),
    )

    def get_bouquet_price(self, obj):
        return obj.bouquet.price if obj.bouquet else "Нет букета"

    get_bouquet_price.short_description = "Цена букета"

    def save_model(self, request, obj, form, change):
        print("test")
        if change:
            old_obj = Order.objects.get(id=obj.id)
            if obj.status != old_obj.status and obj.status == 'confirmed':
                asyncio.run(self.send_telegram_message(obj))
        super().save_model(request, obj, form, change)

    async def send_telegram_message(self, obj):
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        if not bot_token or not chat_id:
            return

        bot = Bot(token=bot_token)
        message = (
            f"Заказ {obj.id} Подтверждён.\n"
            f"client: {obj.client_name}\n"
            f"Phone: {obj.phone_number}\n"
            f"Address: {obj.address}\n"
            f"Bouquet: {obj.bouquet}\n"
            f"Price: {obj.bouquet.price if obj.bouquet else 'Нет букета'}"
        )

        await bot.send_message(chat_id=chat_id, text=message)
        await bot.session.close()


admin.site.register(Bouquet, BouquetAdmin)
admin.site.register(Event)
admin.site.register(Budget)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Order, OrderAdmin)
