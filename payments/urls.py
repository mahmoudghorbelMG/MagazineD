# payments/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test.as_view(), name='test'),
     path('config/', views.stripe_config),  # new
      path('create-checkout-session/', views.create_checkout_session,name='create_checkout_session'), # new
         path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()), # new
       path('under_development/', views.under_development, name='under_development'),
    
]