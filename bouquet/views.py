from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from .models import Bouquet, Event, Budget, Consultation
from .forms import ConsultationForm


def index(request):
    return render(request, "index.html")


def card(request):
    return render(request, "card.html")


def catalog(request):
    return render(request, "catalog.html")


def consultation_view(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ConsultationForm()

    return render(request, 'consultation.html', {'form': form})


def order(request):
    return render(request, "order.html")


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
