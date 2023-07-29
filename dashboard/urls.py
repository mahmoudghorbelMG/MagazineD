from django.urls import path
from . import views
from .views import subscription_confirm
from .views import *
# from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('main/', views.main, name='main'),
    path('dashboard/', views.dashbord, name='dashbord'),
    path('add-article/', views.add_article, name='add_article'),


    path('articles_en_attente', views.articles_en_attente,
         name='articles_en_attente'),

    


    path('update-article/<int:article_id>/',
         views.update_article, name='update_article'),
    path('delete_article/<int:article_id>/',
         views.delete_article, name='delete_article'),

    path('Update', views.Update, name='Update'),
    path('mark_all_as_read/', mark_all_as_read, name='mark_all_as_read'),

    

     path('subscription',views.subscription  , name="subscription") , 
    path('subscribe/', subscription_confirm, name='subscription_confirm'),
    path('article', views.article, name='article'),
    path('add_product', views.add_product, name='add_product'),
    

    path('articles/<int:article_id>/', views.view_article, name='view_article'),

    path('notifiactions', views.notifications, name='notifications'),
    path('search', views.search, name='search'),
    path('search_dashboard', views.search_dashboard, name='search_dashboard'),

    #------------------------------------------ product------------------------------------------#

        path('product', views.product, name='product'),
        path('user_orders', views.user_orders, name='user_orders'),
        path('add_product', views.add_product, name='add_product'),
            path('update-product/<int:product_id>/',
         views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/',
         views.delete_product, name='delete_product'),
    
        path('under_development/', views.under_development, name='under_development'),
    # path('change_password/', PasswordChangeView.as_view(), name='change_password'),




]
