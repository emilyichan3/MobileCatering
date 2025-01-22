from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="orders-home"),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
]