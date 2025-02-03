from django.urls import path
from .views import (
    OrderListView,
    OrderCreatelView,
    OrderUpdateView,
    OrderDeleteView,
    OrderMenuByCatererListView,
    CatererListView,
    MyCatererCreateView,
    MyCatererListView,
    MyCatererUpdateView,
    MyCatererDeleteView,
    MyCatererMenuListView,
    MyCatererMenuCreateView,
    MyCatererMenuUpdateView,
    MyCatererMenuDeleteView,
    MyCatererMenuOrderListView
)
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", CatererListView.as_view(), name='orders-home'),
    path("menu", views.menu, name="orders-menu"),
    path('menu/caterer/<int:caterer_id>/', OrderMenuByCatererListView.as_view(), name='orders-menu-by-caterer'),
    path("myOrder/<int:user_id>/", OrderListView.as_view(), name='orders-myorder'),
    path('myOrder/<int:menu_id>/new/', OrderCreatelView.as_view(), name='orders-myorder-new'),
    path('myOrder/<int:pk>/update/', OrderUpdateView.as_view(), name='orders-myorder-update'),
    path('myOrder/<int:pk>/delete/', OrderDeleteView.as_view(), name='orders-myorder-delete'),
    path('about/',views.about, name='orders-about'),
    path('myCaterer/<int:user_id>/', MyCatererListView.as_view(), name='orders-mycaterer'),
    path('myCaterer/new/', MyCatererCreateView.as_view(), name='orders-mycaterer-new'),
    path('myCaterer/<int:pk>/update/', MyCatererUpdateView.as_view(), name='orders-mycaterer-update'),
    path('myCaterer/<int:pk>/delete/', MyCatererDeleteView.as_view(), name='orders-mycaterer-delete'),
    path('myCaterer/<int:caterer_id>/menu/', MyCatererMenuListView.as_view(), name='orders-mycaterer-menu'),
    path('myCaterer/<int:caterer_id>/menu/new/', MyCatererMenuCreateView.as_view(), name='orders-mycaterer-menu-new'),
    path('myCaterer/<int:caterer_id>/menu/<int:pk>/update/', MyCatererMenuUpdateView.as_view(), name='orders-mycaterer-menu-update'),
    path('myCaterer/<int:caterer_id>/menu/<int:pk>/delete/', MyCatererMenuDeleteView.as_view(), name='orders-mycaterer-menu-delete'),
    path('myCaterer/<int:caterer_id>/menu/<int:menu_id>/orders/', MyCatererMenuOrderListView.as_view(), name='orders-mycaterer-menu-orders'),
]

# below code is for app's iamges using static method
# urlpatterns += staticfiles_urlpatterns() 

