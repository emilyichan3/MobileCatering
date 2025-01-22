from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Order, Menu

def home(request):
    context = {
       'orders': Order.objects.all()
    }
    return render(request, 'orders/home.html', context)

def menu(request):
    context = {
       'menus': Menu.objects.all()
    }
    return render(request, 'orders/menu.html', context)

def about(request):
    return render(request, 'orders/about.html', {'title': 'About'})