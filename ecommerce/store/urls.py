from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path 
from django.conf.urls import url, include
from .views import HomeView, add_to_cart, checkout, detail, favorite, detail_item, list_cart, remove_cart

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cart/<uuid:id>', add_to_cart, name='add_to_cart'),
    path('cart_list/', list_cart, name='list_cart'),
    path('checkout/', checkout, name='store_checkout'),
    path('detail/<uuid:pk>', detail.as_view(), name='store_detail'),
    path('favorite/<uuid:pk>', favorite, name='favorite_annonce'),
    path('remove/<int:id>', remove_cart, name='remove_from_cart'),
    
    
]