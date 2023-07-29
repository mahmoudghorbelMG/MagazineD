from django.urls import path
from . import views
from .views import *
urlpatterns = [

 
path('article/<int:article_id>', views.add_comment, name='add_comment'),
path('', views.Home, name='Home'),
 path('category/<slug:slug>/', views.category_page, name='category_page'),
 path('searchMagazine', views.searchMagazine, name='searchMagazine'),

]