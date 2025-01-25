from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Order, Menu, Caterer
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

User = get_user_model()

class CatererListView(ListView):
    model = Caterer
    template_name = 'orders/home.html' # we can define the template either here or in the urls
    context_object_name = 'caterers'


class CatererMenuListView(ListView):
    model = Menu
    template_name = 'orders/caterer_menu.html'
    context_object_name = 'menus'
    paginate_by = 5

    def get_queryset(self):
        # Get the caterer_id from the URL kwargs
        caterer_id = self.kwargs.get('caterer_id')
        # Ensure the caterer exists
        caterer = get_object_or_404(Caterer, id=caterer_id)
        # Filter menus belonging to the caterer
        return Menu.objects.filter(owner=caterer)

class OrderListView(ListView):
    model = Order
    template_name = 'orders/myorder.html' # we can define the template either here or in the urls
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