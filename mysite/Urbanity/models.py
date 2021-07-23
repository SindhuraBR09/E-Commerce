from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver

# Create your models here.

class Product(models.Model):
    item_name = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    item_image = models.ImageField(null=True, blank = True)
    quantity = models.IntegerField(default=1)

    def add_to_cart(self):
        self.number = self.number -1

    @property
    def imageURL(self):
        try:
            url = self.item_image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.item_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank = True, null=True)
    name =  models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length = 254, null=True)
    phonenumber = models.CharField(max_length=15,null=True)
    otp = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True, null=True)
    transaction_id = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=False, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank = True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null=True)
    quantity = models.IntegerField(default=0, blank = True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, blank = True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def getTotal(self):
        total = self.quantity * self.product.item_price;
        return total;

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.address
