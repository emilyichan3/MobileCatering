from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderMenuByCatererListView,
    CatererListView,
    MyCatererCreateView,
    MyCatererListView,
    MyCatererUpdateView,
    MyCatererDeleteView,
    MyCatererMenuListView,
    MyCatererMenuCreateView,
    MyCatererMenuUpdateView,
    MyCatererMenuDeleteView
)
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", CatererListView.as_view(), name='orders-home'),
    path("myOrder", OrderListView.as_view(), name='orders-myorder'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='orders-detail'),
    path('about/',views.about, name='orders-about'),
    path("menu", views.menu, name="orders-menu"),
    path('menu/caterer/<int:caterer_id>/', OrderMenuByCatererListView.as_view(), name='orders-menu-by-caterer'),
    path('myCaterer/<int:user_id>/', MyCatererListView.as_view(), name='orders-mycaterer'),
    path('myCaterer/new/', MyCatererCreateView.as_view(), name='orders-mycaterer-new'),
    path('myCaterer/<int:pk>/update/', MyCatererUpdateView.as_view(), name='orders-mycaterer-update'),
    path('myCaterer/<int:pk>/delete/', MyCatererDeleteView.as_view(), name='orders-mycaterer-delete'),
    path('myCaterer/<int:caterer_id>/menu/', MyCatererMenuListView.as_view(), name='orders-mycaterer-menu'),
    path('myCaterer/<int:caterer_id>/menu/new/', MyCatererMenuCreateView.as_view(), name='orders-mycaterer-menu-new'),
    path('myCaterer/<int:caterer_id>/menu/<int:pk>/update/', MyCatererMenuUpdateView.as_view(), name='orders-mycaterer-menu-update'),
    path('myCaterer/<int:caterer_id>/menu/<int:pk>/delete/', MyCatererMenuDeleteView.as_view(), name='orders-mycaterer-menu-delete'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 

