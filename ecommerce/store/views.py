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
from django.urls import reverse
from django.template.defaulttags import register

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "store/home.html"
    context_object_name = 'products'
    


class detail(DetailView):
    model = Item
    template_name = 'store/detail.html'
    context_object_name = 'product'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated: 
        # Add in a QuerySet of all the books
            context['count'] = OrderItem.objects.filter(user=self.request.user.profil, selected=False)[:3].count()
        else:
            context['count'] = 0
        return context


@login_required(login_url='login')
def add_to_cart(request, id):
    id= id
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
    
    return redirect(f"/detail/{id}")


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
            favorite_annonce = False
            etat = 0
            if pk:
                favorite_annonce = get_object_or_404(Item, id=pk)
            if favorite_annonce.favorite.filter(pk=request.user.profil.id).exists(): 
                print(f'favorite_annonce exists' )
                print(f'favorite_annonce exists en etat: {favorite_annonce.is_favorite}')
                favorite_annonce.favorite.remove(request.user.profil) 
                favorite_annonce.is_favorite = False
                favorite_annonce.save()
                print(f'maint est en etat {favorite_annonce.is_favorite}') 
            else:
                favorite_annonce.favorite.add(request.user.profil)
                print(f'favorite_annonce exists pas ' )
                favorite_annonce.favorite.add(request.user.profil) 
                favorite_annonce.is_favorite = True
                favorite_annonce.save()
                print(f'maint est en etat {favorite_annonce.is_favorite}')
            if favorite_annonce.is_favorite == True:
                etat = 1
            else:
                etat = 0
            context = {
                        'etat': etat,
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

def checkout(request):
    orderItems = []
    total_cart = 0
    if request.user.is_authenticated:
        orderItems = OrderItem.objects.filter(user=request.user.profil)
        total_cart1 = OrderItem.objects.filter(user=request.user.profil)[0] 
        total_cart = total_cart1.get_total_orderitem()
    else:
        orderItems = []
    if request.method == "POST":
        if request.POST.get('creatornot') == 'on':
            last_name = request.POST.get('last_name')
            first_name = request.POST.get('first_name')
            country = request.POST.get('country')
            adress1 = request.POST.get('adress1')
            adress2 = request.POST.get('adress2')
            state = request.POST.get('city')
            zipCode = request.POST.get('city')
            phone = request.POST.get('phone')
            email = request.POST.get('phone')
            #continue to anonymos user
        else:
            pass

    context = {
        'orderItems': orderItems,
        'total_cart': total_cart,
    }
    return render(request, 'store/checkout.html', context)


@login_required(login_url='account_login')
def item_favorite_list(request):
    """
    """
    user = request.user
    favorite_list = user.profil.favorite.all()
    context = {
        'favorite_list': favorite_list
    }
    return render(request, 'store/favorite.html', context)




@register.filter
def get_range(value):
    if value == None:
        value = 0
    return range(value)
