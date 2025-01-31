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
from datetime import date

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
        # Filter menus belonging to the register
        # formatted_today = timezone.now().strftime("%Y-%m-%d")
        formatted_today = timezone.now().date()
        # Filter the Menu objects
        menus = Menu.objects.filter(
            owner=caterer,
            available_to__gte=formatted_today, 
            # available_to__lte=formatted_today
        ).order_by('-available_from')  # Order by available_from descending
        
        return menus

    def get_context_data(self, **kwargs):
        if not hasattr(self, 'caterer'):
            caterer_id = self.kwargs.get('caterer_id')
            self.caterer = get_object_or_404(Caterer, id=caterer_id)
        # # Call the base implementation to get the default context
        context = super().get_context_data(**kwargs)
        # # Add the caterer's name to the context
        context['caterer_name'] = self.caterer.caterer_name  # Assuming the Caterer model has a 'name' field
        # return context
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

class CatererInfoView(LoginRequiredMixin, CreateView):
    model = Caterer
    fields = ['caterer_name', 'caterer_description','location']
    success_url = "/"

    def form_valid(self, form):
        form.instance.register = self.request.user
        return super().form_valid(form)
    
class CatererUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Caterer
    fields = ['caterer_name', 'caterer_description','location', 'register']

    # def get_queryset(self):
    #         caterer_id = self.kwargs.get('caterer_id')
    #         register = get_object_or_404(User, id=caterer_id)

    #         caterer = Caterer.objects.filter(
    #             owner=register)
            
    #         return caterer

    def  form_valid(self, form):
        form.instance.register = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        caterer = self.get_object()
        return self.request.user == caterer.register 
    