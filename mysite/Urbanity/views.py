from django.shortcuts import render
from django.views.generic import (TemplateView,ListView)
from Urbanity.models import Order, OrderItem, Customer, Product, ShippingAddress
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cartData,cookieCart, guestOrder

# Create your views here.

class StoreListView(ListView):
    model = Product
    template_name = 'store.html'
    items = []
    order = []
    cartItems = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = cartData(self.request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']
        context['productlist'] = Product.objects.all()
        context['cartItems'] = cartItems
        return context


def main(request):
    context={}
    return render(request, 'main.html', context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def updateitem(request):
    data = json.loads(request.body)
    productid = data['productId']
    action=data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productid )
    order, created = Order.objects.get_or_create(customer=customer, completed = False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if (action == "add"):
        orderitem.quantity = orderitem.quantity +1
    elif (action == "remove"):
        orderitem.quantity = orderitem.quantity -1

    orderitem.save()

    if (orderitem.quantity <= 0):
        orderitem.delete()

    return JsonResponse('Item added', safe=False)

def processOrder(request):
    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if (request.user.is_authenticated):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed = False)

    else:
        customer, order = guestOrder(request, data)

    order.transaction_id = transactionId
    total = data['userFormInfo']['total']
    print("Cart totals {} {}".format(total, order.get_cart_total ))
    if (float(total) == float(order.get_cart_total)):
        print("order complete")
        order.completed = True
    order.save()

    ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shippingInfo']['address'],
        city = data['shippingInfo']['city'],
        state = data['shippingInfo']['state'],
        zipcode= data['shippingInfo']['zipcode']
    )


    return JsonResponse('Ordder Processed', safe=False)
