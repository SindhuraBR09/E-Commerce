from django.shortcuts import render, redirect
from django.views.generic import (TemplateView,ListView)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from Urbanity.models import Order, OrderItem, Customer, Product, ShippingAddress
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cartData,cookieCart, guestOrder, send_sms
from .forms import CreateUserForm, UserLoginForm, OTPForm
from django.contrib import messages
import random
# Create your views here.
def login(request):

    register_form = CreateUserForm()
    login_form = UserLoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            print("into reg logic")
            register_form = CreateUserForm(request.POST)
            username = request.POST.get('username')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phonenumber')

            if register_form.is_valid():
                print("Saving form")
                user = register_form.save()
                customer = Customer.objects.create(name=username, email=email, phonenumber = phonenumber)
                customer.user = user
                customer.save()
                return redirect('login')
            else:
                print(register_form.errors)
                print("form not saved")
        elif 'login' in request.POST:
                print('into login logic')
                login_form = UserLoginForm(request.POST)

                username = request.POST.get('username')
                password = request.POST.get('password1')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    print("logging in")
                    # auth_login(request, user)
                    user.customer.otp = random.randint(1000, 9999)
                    user.customer.save()
                    print("Sindhura new otp {}".format(user.customer.otp))
                    request.session['pk'] = user.pk
                    return redirect('verify')
                else:
                    print("error in login")
                    messages.error(request,'username or password not correct')
                    return redirect('login')
        else:
            print("Nothing")

    context = {'register_form':register_form, 'login_form':login_form}
    return render(request, 'login.html', context)

def verify_user(request):
    verify_form = OTPForm(request.POST)
    pk = request.session.get('pk')
    if pk:
        # user = User.objects.get(pk=pk)
        print("Sindhura pk value {}".format(pk))
        user = User.objects.get(pk=pk)
        customer = user.customer
        code = customer.otp
        if not request.POST:
            send_sms(code, customer.phonenumber)
            print("Username and code {} {}".format(user.username, code))

        if verify_form.is_valid():

            otp = verify_form.cleaned_data.get('otp')

            if (otp == code):
                auth_login(request, user)
                return redirect('products')
            else:
                return redirect('verify')
    context = {'verify_form':verify_form}
    return render(request, 'verify.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

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
        context['productlist'] = Product.objects.all().order_by('item_name')
        context['cartItems'] = cartItems
        return context


def main(request):
    context={}
    return render(request, 'home.html', context)

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

def show(request, id):
    obj = Product.objects.get(id=id )
    context={'product':obj}
    return render(request, 'product-detail.html', context)

def search(request):
    product = request.GET.get('product')
    if product:
        payload=[]
        results = Product.objects.filter(item_name__icontains=product).values()
        # results = results.values_list('item_name')
        for result in results:
            payload.append(result)

    return JsonResponse({'status':200, 'data':payload})

def showSearchedProduct(request):
    data = json.loads(request.body)
    productName = data['productName']
    product = Product.objects.get(item_name=productName)
    return JsonResponse({'status':200 , 'data': product.id})
