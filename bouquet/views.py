from django.shortcuts import render
from .models import Event, Budget

def index(request):
    return render(request, 'index.html')

def card(request):
    return render(request, 'card.html')

def catalog(request):
    return render(request, 'catalog.html')

def consultation(request):
    return render(request, 'consultation.html')

def order(request):
    return render(request, 'order.html')

def order_step(request):
    return render(request, 'order-step.html')


def quiz(request):
    events = Event.objects.all()
    budgets = Budget.objects.all()

    if request.method == 'POST':
        selected_event = request.POST.get('event')
        selected_budget = request.POST.get('budget')

        if selected_event:
            request.session['selected_event'] = selected_event
            return render(request, 'quiz-step.html', {'budgets': budgets})

        if selected_budget:
            request.session['selected_budget'] = selected_budget
            return render(request, 'result.html', {
                'event': request.session.get('selected_event'),
                'budget': selected_budget,
            })

    step = request.GET.get('step', 'event')

    if step == 'event':
        return render(request, 'quiz.html', {'events': events})
    elif step == 'budget':
        return render(request, 'quiz-step.html', {'budgets': budgets})

    return render(request, 'quiz.html', {'events': events})
