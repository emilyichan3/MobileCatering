from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Order, Menu, Caterer
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.models import User #The user model will be the sender
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import MenuCreateForm, OrderCreateForm
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError

User = get_user_model()

class CatererListView(ListView):
    model = Caterer
    template_name = 'orders/home.html' # we can define the template either here or in the urls
    context_object_name = 'caterers'


class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'orders/myOrder_list.html' # we can define the template either here or in the urls
    context_object_name = 'orders'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        # Filter the Caterer objects
        orders = Order.objects.filter(
            customer=user,
        ).order_by('pick_up_at')
        return orders
    
    def test_func(self):
        return self.request.user.id == self.kwargs.get('user_id')


class OrderCreatelView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/myOrder_form.html'
    form_class = OrderCreateForm

    def get_success_url(self):
        return reverse("orders-myorder", kwargs={"user_id": self.request.user.id})
    
    def get_form_kwargs(self):
        # Pass menu instance to form
        kwargs = super().get_form_kwargs()
        menu = get_object_or_404(Menu, id=self.kwargs.get('menu_id'))
        kwargs['menu'] = menu 
        return kwargs

    def get_context_data(self, **kwargs):
        # Pass menu instance to template
        context = super().get_context_data(**kwargs)
        self.menu = get_object_or_404(Menu, id=self.kwargs.get('menu_id'))
        context['menu'] = self.menu
        return context
    
    def form_valid(self, form):
        menu = get_object_or_404(Menu, id=self.kwargs.get('menu_id'))
        form.instance.menu = menu
        form.instance.customer = self.request.user
        form.instance.status = "Ordered"
        if form.instance.pick_up_at > menu.available_to:
            messages.error(self.request, f"The pick-up date must be on or before the menu's available date.: {menu.available_to.strftime('%Y-%m-%d')}.")
            return redirect(reverse("orders-myorder-new", kwargs={"menu_id": self.kwargs.get('menu_id')}))
        return super().form_valid(form)
    

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    template_name = 'orders/myOrder_form.html'
    form_class = OrderCreateForm

    def get_success_url(self):
        return reverse("orders-myorder", kwargs={"user_id": self.request.user.id})
    
    def get_form_kwargs(self):
        # Pass menu instance to form
        kwargs = super().get_form_kwargs()
        menu = get_object_or_404(Menu, id=self.object.menu.id)
        kwargs['menu'] = menu  
        return kwargs

    def get_context_data(self, **kwargs):
        # Pass menu instance to template
        context = super().get_context_data(**kwargs)
        self.menu = get_object_or_404(Menu, id=self.object.menu.id)
        context['menu'] = self.menu

        total_saving = (self.menu.unit_price - self.object.unit_discount_price) * self.object.order_qualities
        context['total_saving'] = total_saving
        
        return context


    def test_func(self):
        order = self.get_object()
        return self.request.user == order.customer 
    
    def form_valid(self, form):
        menu = get_object_or_404(Menu, id=self.object.menu.id)
        if form.instance.pick_up_at > menu.available_to:
            messages.error(self.request, f"The pick-up date must be on or before the menu's available date: {menu.available_to.strftime('%Y-%m-%d')}.")
            return redirect(reverse("orders-myorder-update", kwargs={"pk":self.kwargs.get('pk')}))
        return super().form_valid(form)
  

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'orders/myOrder_confirm_delete.html'

    def get_success_url(self):
        return reverse("orders-myorder", kwargs={"user_id": self.request.user.id})
   
    def test_func(self):
        order = self.get_object()
        return self.request.user == order.customer 
           
    def form_valid(self, form):
        return super().form_valid(form)  # Proceed with deletion if no menus exist
    

class OrderMenuByCatererListView(ListView):
    model = Menu
    template_name = 'orders/menu_by_caterer.html'
    context_object_name = 'menus'

    def get_queryset(self):
        # Get the caterer_id from the URL kwargs
        caterer_id = self.kwargs.get('caterer_id')
        # Ensure the caterer exists
        caterer = get_object_or_404(Caterer, id=caterer_id)
        # Filter menus belonging to the register
        formatted_today = timezone.now().date()
        # Filter the Menu objects
        menus = Menu.objects.filter(
            caterer=caterer,
            available_to__gte=formatted_today, 
            # available_to__lte=formatted_today
        ).order_by('-available_from')  # Order by available_from descending
        
        return menus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caterer_id = self.kwargs.get('caterer_id')
        # Fetch caterer only once
        if not hasattr(self, 'caterer'):
            self.caterer = get_object_or_404(Caterer, id=caterer_id)

        context['caterer_name'] = self.caterer.caterer_name  # Ensure the field exists in your model
        return context


class menu(ListView):
    model = Menu
    template_name = 'orders/menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        formatted_today = timezone.now().date()
        # Filter the Menu objects
        menus = Menu.objects.filter(
            available_to__gte=formatted_today, 
        )
        
        return menus


class MyCatererCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Caterer
    template_name = 'orders/myCaterer_form.html'
    fields = ['caterer_name', 'caterer_description','location']
    success_url = "/"

    permission_required = 'orders.add_caterer'  # Ensure correct app_label

    def form_valid(self, form):
        form.instance.register = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("orders-mycaterer", kwargs={"user_id": user_id})

    
class MyCatererListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Caterer
    template_name = 'orders/myCaterer_list.html'
    context_object_name = 'caterers'

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        # Filter the Caterer objects
        caterers = Caterer.objects.filter(
            register=user,
        )
        return caterers
    
    def test_func(self):
        return self.request.user.id == self.kwargs.get('user_id')


class MyCatererUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Caterer
    template_name = 'orders/myCaterer_form.html'
    fields = ['caterer_name', 'caterer_description','location']

    def form_valid(self, form):
        form.instance.register = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        caterer = self.get_object()
        return self.request.user == caterer.register 
    
    
class MyCatererDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Caterer
    template_name = 'orders/myCaterer_confirm_delete.html'

    def get_success_url(self):
        """Dynamically generate the success URL with user_id."""
        user_id = self.request.user.id
        return reverse("orders-mycaterer", kwargs={"user_id": user_id})
    
    def test_func(self):
        caterer = self.get_object()
        return self.request.user == caterer.register
    
    def form_valid(self, form):
        caterer = self.get_object()

        if caterer.menu.all().exists():  
            messages.error(self.request, "This caterer cannot be deleted because it has linked menus.")
            return redirect(reverse("orders-mycaterer", kwargs={"user_id": caterer.register.id}))
        return super().form_valid(form)  # Proceed with deletion if no menus exist
    

class MyCatererMenuListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Menu
    template_name = 'orders/myCaterer_menu.html'
    context_object_name = 'menus'

    def get_queryset(self):
        # Get the caterer_id from the URL kwargs
        caterer_id = self.kwargs.get('caterer_id')
        # Ensure the caterer exists
        caterer = get_object_or_404(Caterer, id=caterer_id)
        # Filter the Menu objects
        menus = Menu.objects.filter(
            caterer=caterer,
        )
        return menus

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caterer_id = self.kwargs.get('caterer_id')
        # Fetch caterer only once
        if not hasattr(self, 'caterer'):
            self.caterer = get_object_or_404(Caterer, id=caterer_id)

        context['caterer'] = self.caterer
        return context
    
    def test_func(self):
        caterer_id = self.kwargs.get('caterer_id') 
        caterer = get_object_or_404(Caterer, id=caterer_id)
        return self.request.user == caterer.register  # Check if the logged-in user is the caterer


class MyCatererMenuCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Menu
    template_name = 'orders/myCaterer_menu_form.html'
    form_class = MenuCreateForm
    success_url = "/"

    def get_queryset(self):
        caterer = get_object_or_404(Caterer, register=self.request.user)
        return Menu.objects.filter(caterer=caterer) 
    
    def form_valid(self, form):
        caterer_id = self.kwargs.get('caterer_id')
        caterer = get_object_or_404(Caterer, id=caterer_id)
        form.instance.caterer = caterer
        form.instance.register = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        caterer_id = self.kwargs.get('caterer_id')
        return reverse("orders-mycaterer-menu", kwargs={"caterer_id": caterer_id})
    
    def test_func(self):
        caterer_id = self.kwargs.get('caterer_id') 
        caterer = get_object_or_404(Caterer, id=caterer_id)
        return self.request.user == caterer.register  # Check if the logged-in user is the caterer

class MyCatererMenuUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    template_name = 'orders/myCaterer_menu_form.html'
    form_class = MenuCreateForm

    def get_success_url(self):
        menu = get_object_or_404(Menu, id=int(self.kwargs.get('pk')))
        return reverse("orders-mycaterer-menu", kwargs={"caterer_id": menu.caterer.id})
    
    def test_func(self):
        caterer = self.get_object()
        return self.request.user == caterer.register 
    
    def form_valid(self, form):
        caterer_id = self.kwargs.get('caterer_id')
        menu = self.get_object()
       
        if any(form.instance.available_to < order.pick_up_at for order in menu.orders.all()):
            messages.error(self.request, "Menu update failed: Some orders have pick-up dates that are later than the menu's available date.")
            return redirect(reverse("orders-mycaterer-menu", kwargs={"caterer_id": caterer_id}))

        return super().form_valid(form)  
    
class MyCatererMenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Menu
    template_name = 'orders/myCaterer_menu_confirm_delete.html'

    def get_success_url(self):
        caterer_id = self.kwargs.get('caterer_id')
        return reverse("orders-mycaterer-menu", kwargs={"caterer_id": caterer_id})
    
    def test_func(self):
        caterer = self.get_object()
        return self.request.user == caterer.register
    
    def form_valid(self, form):
        caterer_id = self.kwargs.get('caterer_id')
        menu = self.get_object()

        if menu.orders.all().exists():  
            messages.error(self.request, "This menu cannot be deleted because it has existing orders.")
            return redirect(reverse("orders-mycaterer-menu", kwargs={"caterer_id": caterer_id}))
        return super().form_valid(form)  # Proceed with deletion if no menus exist


class MyCatererMenuOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'orders/myCaterer_menu_orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        menu = get_object_or_404(Menu, id=self.kwargs.get('menu_id'))
        # Filter the Caterer objects
        orders = Order.objects.filter(
            menu=menu,
        )
        return orders
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caterer_id = self.kwargs.get('caterer_id')

        context['caterer_id'] = caterer_id
        return context
    
    def test_func(self):
        caterer_id = self.kwargs.get('caterer_id') 
        caterer = get_object_or_404(Caterer, id=caterer_id)
        return self.request.user == caterer.register  # Check if the logged-in user is the caterer
