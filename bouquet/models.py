from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False,
                             null=False, verbose_name="Название")

    def __str__(self):
        return str(self.title)


class Bouquet(models.Model):
    STATUS = (
        ("NEW", "Новый"),
        ("PAY", "Оплачен"),
        ("CFM", "Подтвержден"),
        ("COM", "Завершен"),
    )
    title = models.CharField(max_length=100, blank=False,
                             null=False, verbose_name="Название")
    price = models.DecimalField(
        blank=False, null=False, max_digits=8, decimal_places=2, verbose_name="Цена")
    status = models.CharField(
        max_length=3, choices=STATUS, default="NEW", verbose_name="Статус", db_index=True)
    composition_description = models.TextField(
        blank=False, null=False, verbose_name="Состав")
    image = models.ImageField(upload_to="images/")
    size_description = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Размер")
    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return str(self.title)
