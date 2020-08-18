from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path 
from django.conf.urls import url, include
from .views import home, cart, checkout, detail_product, favorite

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='store_cart'),
    path('checkout/', checkout, name='store_checkout'),
    path('detail/<int:id>', detail_product, name='store_detail'),
    path('favorite/<int:pk>', favorite, name='favorite_annonce'),
]