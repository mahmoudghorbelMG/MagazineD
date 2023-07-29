from django.urls import path
from . import views
from .views import *

# from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path("tracker-bar/", tracker_bar_view, name="tracker-bar"),
    path("currencies", currencies, name="currencies"),
    path("stocks_list/", stocks_list, name="stocks_list"),
    path('crypto_data_view/', crypto_data_view, name='crypto_data_view'),
     path('trending', trending, name='trending'),
]
