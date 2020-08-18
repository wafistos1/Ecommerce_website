from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    OUT_OF_STOK = 'OUT OF STOK'
    NEW = 'NEW'
    LABEL_CHOICES = [
        (OUT_OF_STOK, 'OUT OF STOK'),
        (NEW, 'NEW'),
        ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    short_description = models.TextField(default='', null=True, blank=True)
    nb_products = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=200, null=True, blank=True, choices=LABEL_CHOICES)
    favorite = models.ManyToManyField(Customer, related_name='favorite', blank=True)


    def get_image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
 
    def get_absolute_url(self):  # new
        return reverse('store_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    # def get_favorite_url(self):  # new
    #     return reverse('favorite_annonce', args=[str(self.id)])
    
    # def get_update_url(self):  # new
    #     return reverse('annonce_update', args=[str(self.id)])
    
    # def get_delete_url(self):  # new
    #     return reverse('annonce_delete', args=[str(self.id)])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="orderitem")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"{self.id}- {self.product.name}- owner:{self.order.customer.name}"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class ImageProduct(models.Model):
    annonce_images = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    image = models.FileField(upload_to='image/', default='image_default.jpg', blank=True, null=True)
    
    class Meta:
        pass

    def __str__(self):
        return self.annonce_images.name
