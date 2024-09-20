## Чтобы загрузить цветы:

```
python manage.py migrate
python manage.py loaddata bouquets.json
cp -R images /media/images
```

## Чтобы работала оплата:
Файл .env 

YOOKASSA_SECRET_KEY= ключ для магаза
YOOKASSA_SHOP_ID=айди магаза
