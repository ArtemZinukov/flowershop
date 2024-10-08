from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from bouquet import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('card/<int:pk>/', views.CardView.as_view(), name='card'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('consultation/', views.consultation_view, name='consultation'),
    path('create-order/', views.create_order, name='order'),
    path('order_step/', views.order_step, name='order_step'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/step/', views.quiz, name='quiz-step')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
