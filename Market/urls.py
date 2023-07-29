from django.urls import path
from . import views
from .views import *



urlpatterns = [

      path('market/', views.market, name='market'),
    path('shop/', views.shop, name='shop'),
    path('check/', views.check, name='check'),
    path('place_order/', views.place_order, name='place_order'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
     path('details/<int:product_id>/', views.details, name='details'),
      path('market/search/', views.searchMarket, name='search_market'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),


]
