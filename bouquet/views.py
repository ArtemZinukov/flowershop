from django.shortcuts import render

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