from django.contrib import admin
from .models import Item, OrderItem, Order, ShippingAddress, ImagesItem, Rating
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(ShippingAddress)
admin.site.register(ImagesItem)
admin.site.register(Rating) 