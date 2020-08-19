from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from store.models import OrderItem, Order, Product, ShippingAddress
from django.contrib.auth.decorators import login_required
from register.models import Customer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse

def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/home.html', context)

@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_item, created = OrderItem.objects.get_or_create(product=product, owner=request.user.customer)
    order_item.quantity += 1
    order_item.save()
    product_items_cart = OrderItem.objects.filter(owner=request.user.customer)

    context = {
        'products': product_items_cart
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        print('je suis dans le if user')
        customer = request.user.customer
        order = Order.objects.filter(customer=customer)
        print(order.customer.name)
        order = order.orderitem.all()
    else:
        order = []
    
    items = OrderItem.objects.all()
    
    context = {
        'items': items,
        'order': order,

    }
    return render(request, 'store/checkout.html', context)


def detail_product(request, id):
    """
    """
    product = None
    if id:
        product = get_object_or_404(Product, id=id)
    
    if product.favorite.filter(id=request.user.id).exists():
        product.is_favorite = True
        product.save()
    else:
        print('favorite is now False')


    context = {
        
        'product': product

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
        favorite_annonce = get_object_or_404(Product, id=pk)
    print(f'favorite_annonce: {favorite_annonce}' )
    # # Verifier si l'object existe dans la BD 
    # print('je suis dans favorite views')
    if favorite_annonce.favorite.filter(id=request.user.customer.id).exists():
        
        favorite_annonce.favorite.remove(request.user.customer.id)
        favorite_annonce.is_favorite = False
        favorite_annonce.save()
    else:
        
        favorite_annonce.favorite.add(request.user.customer.id)
        favorite_annonce.is_favorite = True
        favorite_annonce.save()
        print(f' Etat du favorite {favorite_annonce.favorite}' )
    context = {
            'etat': favorite_annonce.is_favorite,
        }
    dump = json.dumps(context)
    return HttpResponse(dump, content_type='applicaion/json')