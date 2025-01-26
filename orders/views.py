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
from django.db.models import Q
from django.utils import timezone

User = get_user_model()

class CatererListView(ListView):
    model = Caterer
    template_name = 'orders/home.html' # we can define the template either here or in the urls
    context_object_name = 'caterers'

class CatererMenuListView(ListView):
    model = Menu
    template_name = 'orders/caterer_menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        # Get the caterer_id from the URL kwargs
        caterer_id = self.kwargs.get('caterer_id')
        # Ensure the caterer exists
        caterer = get_object_or_404(Caterer, id=caterer_id)
        # Filter menus belonging to the caterer
        formatted_today = timezone.now().strftime("%Y-%m-%d")
        # Filter the Menu objects
        menus = Menu.objects.filter(
            owner=caterer,
            available_from__gte=formatted_today  # Use __gte (greater than or equal)
        ).order_by('-available_from')  # Order by available_from descending
        
        return menus

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'caterer'):
            caterer_id = self.kwargs.get('caterer_id')
            self.caterer = get_object_or_404(Caterer, id=caterer_id)
        # Call the base implementation to get the default context
        context = super().get_context_data(**kwargs)
        # Add the caterer's name to the context
        context['caterer_name'] = self.caterer.caterer_name  # Assuming the Caterer model has a 'name' field
        return context
    

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