from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    CatererListView,
    CatererMenuListView,
    CatererInfoView,
    CatererUpdateView
)
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", CatererListView.as_view(), name='orders-home'),
    path("myOrder", OrderListView.as_view(), name='orders-myorder'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
    path('caterer/<int:caterer_id>/menus/', CatererMenuListView.as_view(), name='orders-caterer-menu'),
    path('caterer/', CatererInfoView.as_view(), name='caterer-info'),
    path('caterer/<int:pk>/update/', CatererUpdateView.as_view(), name='caterer-info-update'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 

