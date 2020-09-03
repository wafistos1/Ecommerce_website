from store.models import OrderItem, Item
from django import  template

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user.profil, ordered=False)
        if qs.exists():
            return qs.count()
            
        return 0


@register.filter
def item_favorite_count(user):
    if user.is_authenticated:
        qs = Item.objects.filter(favorite=user.profil) 
        if qs.exists():
            return qs.count()
            
        return 0