from django.shortcuts import render, redirect

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
    if request.method == 'POST':

        selected_event = request.POST.get('event')

        if selected_event:
            return render(request, 'quiz-step.html')

    step = request.GET.get('step', 'event')

    if step == 'event':
        return render(request, 'quiz.html')
