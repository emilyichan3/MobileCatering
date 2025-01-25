from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    CatererListView,
    CatererMenuListView
)
from . import views

urlpatterns = [
    path("", CatererListView.as_view(), name='orders-home'),
    path('caterer/<int:caterer_id>/menus/', CatererMenuListView.as_view(), name='orders-caterer-menu'),
    path("myorder", OrderListView.as_view(), name='orders-myorder'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
]