from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
import json
from django.db.models import Sum
from store.models import OrderItem, Order, Item, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from register.models import Profil
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core import serializers

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "store/home.html"
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs) 
        # Add in a QuerySet of all the books 
        if self.request.user.profil: 
            context['orderItems'] = OrderItem.objects.filter(user=self.request.user.profil).order_by('-id')[:3] 
            context['count'] = OrderItem.objects.filter(user=self.request.user.profil, selected=False).count()
        return context


class detail(DetailView):
    model = Item
    template_name = 'store/detail.html'
    context_object_name = 'product'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['count'] = OrderItem.objects.filter(user=self.request.user.profil, selected=False)[:3].count()
        return context


@login_required(login_url='login')
def add_to_cart(request, id):
    if request.is_ajax():
        print(request.POST.get('pk'))
        pk = request.POST.get('pk')
        item = get_object_or_404(Item, id=pk)
        order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user.profil)
        if order_item.quantity == 0:
            order_item.quantity = 1
        else:
            order_item.quantity += 1
        order_item.save()
        item_items_cart = OrderItem.objects.get(user=request.user.profil, item=item)
        item_title = item_items_cart.item.title
        item_price = item_items_cart.item.price
        id_order = item_items_cart.id
        context = {
            'item_title': item_title,
            'item_price': item_price,
            'count': OrderItem.objects.filter(user=request.user.profil, selected=False).count(),
            'id': id_order, 
            # 'item_image_url': item_image_url,
        } 
        return JsonResponse(context)
    return redirect('store_detail')


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

    countItem = OrderItem.objects.filter(user=request.user.profil, selected=False)
    print(f'count {countItem.count()}')
    context = {
        
        'item': item,
        'count': countItem.count(),
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
        if request.is_ajax():
            favorite_annonce = None
            if pk:
                favorite_annonce = get_object_or_404(Item, id=pk)
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
            return JsonResponse(context)
        else:
            messages.add_message(request, messages.ERROR, "ERROR REQUEST'")
        return render(request, 'store/cart.htm')


@login_required(login_url='login')
def list_cart(request):

    orderItems = OrderItem.objects.filter(user=request.user.profil)
    if request.is_ajax():
        print('if ajax cart update')
        for order in orderItems:
            order.selected = True
            order.save()
    countItem = OrderItem.objects.filter(user=request.user.profil, selected=False)
    total_cart1 = OrderItem.objects.filter(user=request.user.profil)
    total_cart = 0
    for total in total_cart1:
        total_cart += total.get_total_item_price() 
    print(total_cart1, )
    # total_cart = total_cart2 * total_cart1
    print(countItem)
    context = {
        'items': orderItems,
        'count': countItem.count(),
        'total_cart': total_cart, 
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def remove_cart(request, id):
    if request.method == "GET":
        remove_item = get_object_or_404(OrderItem, id=id)
        if remove_item.user == request.user.profil:
            remove_item.delete()
            print(f'ItemOreder {remove_item} are deleted')
            messages.add_message(request, messages.SUCCESS, f' {remove_item.item.title} are DELETED')
        return redirect('list_cart')
    else:
        messages.add_message(request, messages.ERROR, "YOU CANT DELETE THIS ITEM'")
    context = {
    }
    return render(request, 'store/cart.html', context)


def update_item(request):
    if request.is_ajax():
        print(request.POST)
        id = request.POST['id']
        quantity = request.POST['indent']
        action = request.POST['action']

        
        orderItem = get_object_or_404(OrderItem, id=id)
        quantity = None 
        if orderItem.user == request.user.profil:
            if action == 'inc qtybtn':
                orderItem.quantity += 1
                orderItem.save()
                
            elif action == 'dec qtybtn':
                if orderItem.quantity <= 0:
                    orderItem.quantity = 0
                else:
                    orderItem.quantity -= 1
                orderItem.save()
                
            else:
                pass
        quantity = orderItem.quantity
        total = orderItem.get_total_item_price()
        tatal = float(total)
        quantity = int(quantity)
        id_item = int(orderItem.id)
        total_cart1 = OrderItem.objects.filter(user=request.user.profil)[0] 
        total_cart = total_cart1.get_total_orderitem()
        
        total_cart = float(total_cart) 
        print(id_item)
        print(tatal)
        print(total_cart)
        # print(type(total_cart))
        context = {
            'quantity': quantity,
            'id': id_item,
            'total': total,
            'total_cart': total_cart,
            }
        
        return JsonResponse(context)
    context = {

        }
    return render(request, 'store/cart.html', context)