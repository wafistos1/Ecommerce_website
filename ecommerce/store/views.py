from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from store.models import Customer, OrderItem, Order, Product, ShippingAddress
# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/home.html', context)


def cart(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/cart.html', context)


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
    product = get_object_or_404(Product, id=id)
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        is_favorite = True
    else:
        print('favorite is now False')


    context = {
        'is_favorite': is_favorite,
        'product': product

    }
    return render(request, 'store/detail.html', context)


def favorite(request, pk):
    """
    """
    favorite_annonce = get_object_or_404(Product, id=pk)
    print(f'favorite_annonce: {favorite_annonce}' )
    # # Verifier si l'object existe dans la BD 
    # print('je suis dans favorite views')
    if favorite_annonce.favorite.filter(id=request.user.id).exists():
        print('je suis dans favorite qui vaux True')
        favorite_annonce.favorite.remove(request.user.id)
    else:
        print('je suis dans favorite qui vaux False')
        favorite_annonce.favorite.add(request.user.id)
        print(f' Etat du favorite {favorite_annonce.favorite}' )
    return HttpResponseRedirect(favorite_annonce.get_absolute_url())