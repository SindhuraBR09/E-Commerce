from django.contrib import admin
from Urbanity.models import Order, OrderItem, Customer, Product, ShippingAddress

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ShippingAddress)
# Register your models here.
