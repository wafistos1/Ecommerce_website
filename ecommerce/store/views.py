from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from store.models import OrderItem, Order, Item, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from register.models import Profil
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "store/home.html"
    context_object_name = 'products'

class detail(DetailView):
    model = Item
    template_name = 'store/detail.html'
    context_object_name = 'product'

@login_required(login_url='login')
def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user.profil)
    if order_item.quantity == 0:
        order_item.quantity = 1
    else:
        order_item.quantity += 1
    order_item.save()
    item_items_cart = OrderItem.objects.filter(user=request.user.profil)

    context = {
        'items': item_items_cart
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        print('je suis dans le if user')
        profil = request.user.profil
        order = Order.objects.filter(profil=profil)
        print(order.profil.username)
        order = order.orderitem.all()
    else:
        order = []
    
    items = OrderItem.objects.all()
    
    context = {
        'items': items,
        'order': order,

    }
    return render(request, 'store/checkout.html', context)


def detail_item(request, id):
    """
    """
    item = None
    if id:
        item = get_object_or_404(Item, id=id)
    
    if item.favorite.filter(id=request.user.id).exists():
        item.is_favorite = True
        item.save()
    else:
        print('favorite is now False')


    context = {
        
        'item': item

    }
    return render(request, 'store/detail.html', context)


@csrf_exempt
@login_required(login_url='login')
def favorite(request, pk):
    """
    """

    if request.method == "POST":
        val = request.POST.get('val')
        print(val)
    favorite_annonce = None
    if pk:
        favorite_annonce = get_object_or_404(Item, id=pk)
    print(f'favorite_annonce: {favorite_annonce}' )
    # # Verifier si l'object existe dans la BD 
    # print('je suis dans favorite views')
    
    if favorite_annonce.favorite.filter(id=request.user.profil.id).exists():
        print(f'favorite_annonce exists en etat: {favorite_annonce.is_favorite}' )
        favorite_annonce.favorite.remove(request.user.profil.id)
        favorite_annonce.is_favorite = False
        favorite_annonce.save()
    else:
        
        favorite_annonce.favorite.add(request.user.profil.id)
        print(f'favorite_annonce exists pas : {favorite_annonce.is_favorite}' )

        favorite_annonce.is_favorite = True
        favorite_annonce.save()
    context = {
            'etat': favorite_annonce.is_favorite,
        }
    dump = json.dumps(context)
    return HttpResponse(dump, content_type='text/html')