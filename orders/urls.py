from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    CatererListView,
    MyCatererCreateView,
    MyCatererListView,
    MyCatererMenuListView,
    MyCatererUpdateView,
    MyCatererDeleteView
)
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", CatererListView.as_view(), name='orders-home'),
    path("myOrder", OrderListView.as_view(), name='orders-myorder'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
    path('myCaterer/<int:user_id>/', MyCatererListView.as_view(), name='orders-mycaterer'),
    path('myCaterer/new/', MyCatererCreateView.as_view(), name='orders-mycaterer-new'),
    path('myCaterer/caterer/<int:caterer_id>/menus/', MyCatererMenuListView.as_view(), name='orders-mycaterer-menu'),
    path('myCaterer/<int:pk>/update/', MyCatererUpdateView.as_view(), name='orders-mycaterer-update'),
    path('myCaterer/<int:pk>/delete/', MyCatererDeleteView.as_view(), name='orders-mycaterer-delete'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 

