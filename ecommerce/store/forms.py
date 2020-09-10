
from django.contrib.auth.models import User
from django import forms
from register.models import Profil
from .models import ShippingAddress, Order, OrderItem
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class adressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fiels = ('address', 'address1', 'city', 'state', 'phone', 'zipcode')
        exclude = ['profil']

class CheckoutForm(forms.Form):
    

    adress1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'adress1',
        'placeholder':"Street Address"
        
        }))

    adress2 = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'adress2',
        'placeholder':"Apartment. suite, unite ect ( optinal )"
        
        }))
    city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'city',
        
        }))

    country = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'country',
        
        }))
    zip_code = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
    'class': 'checkout__form__input',
    'name': 'zip_code',
    
    }))
    phone = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'phone',
        
        }))
    email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'checkout__form__input',
        'name': 'phone',
        
        }))


