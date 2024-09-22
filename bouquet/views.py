from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Bouquet, Event, Budget, Order
from .forms import ConsultationForm
from yookassa import Configuration, Payment

Configuration.configure(settings.YOOKASSA_SHOP_ID,
                        settings.YOOKASSA_SECRET_KEY)


def consultation_view(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ConsultationForm()

    return render(request, 'consultation.html', {'form': form})


def create_order(request):
    if request.method == 'POST':
        client_name = request.POST.get('fname')
        phone_number = request.POST.get('tel')
        address = request.POST.get('adres')
        order_time = request.POST.get('orderTime')
        bouquet_id = request.POST.get('bouquet_id')

        bouquet = Bouquet.objects.get(id=bouquet_id)

        order = Order(client_name=client_name, phone_number=phone_number,
                      address=address, order_time=order_time, bouquet=bouquet)
        order.save()

        payment = Payment.create({
            "amount": {
                "value": str(bouquet.price),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri('/')
            },
            "capture": True,
            "description": f"Заказ от {client_name}"
        })

        return redirect(payment.confirmation.confirmation_url)

    else:
        bouquet_id = request.GET.get('bouquet')

    return render(request, 'order.html', {'bouquet_id': bouquet_id})


def order_step(request):
    return render(request, "order-step.html")


def quiz(request):
    events = Event.objects.all()
    budgets = Budget.objects.all()

    event_name = request.GET.get("event")
    budget = request.GET.get("budget")

    if event_name and budget:
        try:
            bouquet = (
                Bouquet.objects.filter(events__title=event_name)
                .filter(price__lt=int(budget))
                .order_by("-price")
                .prefetch_related(Prefetch("events", queryset=events.filter(title=event_name)))
                .first()
            )
        except ValueError:
            bouquet = None

        if not bouquet:
            bouquet = Bouquet.objects.order_by("?").first()
        return render(request, "result.html", {"bouquet": bouquet})

    if event_name:
        try:
            event = events.get(title=event_name)
        except Event.DoesNotExist:
            return render(request, "quiz.html", {"events": events})
        return render(request, "quiz-step.html", {"budgets": budgets, "event": event})

    return render(request, "quiz.html", {"events": events})


class CatalogView(ListView):
    model = Bouquet
    template_name = "catalog.html"
    context_object_name = "bouquets"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if self.request.GET.get("all") else queryset[:6]


class CardView(DetailView):
    model = Bouquet
    template_name = "card.html"
    context_object_name = "bouquet"


class Index(ListView):
    model = Bouquet
    template_name = "index.html"
    context_object_name = "bouquets"

    def get_queryset(self):
        return super().get_queryset()[:3]
