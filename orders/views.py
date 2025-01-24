from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, Menu
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OrderListView(ListView):
    model = Order
    template_name = 'orders/home.html' # we can define the template either here or in the urls
    context_object_name = 'orders'
    ordering = ['-order_at']


class OrderDetailView(DetailView):
    model = Order


def menu(request):
    context = {
       'menus': Menu.objects.all()
    }
    return render(request, 'orders/menu.html', context)

def about(request):
    return render(request, 'orders/about.html', {'title': 'About'})