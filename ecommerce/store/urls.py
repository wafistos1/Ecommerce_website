
from django.urls import path
from .views import HomeView, add_to_cart, checkoutView, detail, favorite, list_cart, remove_cart, update_item, item_favorite_list


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cart/<uuid:id>', add_to_cart, name='add_to_cart'),
    path('cart_list/', list_cart, name='list_cart'),
    path('checkout/', checkoutView.as_view(), name='store_checkout'),
    path('detail/<uuid:pk>', detail.as_view(), name='store_detail'),
    path('favorite/<uuid:pk>', favorite, name='favorite_annonce'),
    path('remove/<int:id>', remove_cart, name='remove_from_cart'),
    path('update_item/', update_item, name='update_item'),
    path('favorite/', item_favorite_list, name='item_favorite'),
]