from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView
)
from . import views

urlpatterns = [
    path("", OrderListView.as_view(), name='orders-home'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
]