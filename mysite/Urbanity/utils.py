from . models import *
import json
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        print("setting cart to {}")
        cart = {}
    # cart = json.loads(request.COOKIES['cart'])
    print(cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:

            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.item_price * cart[i]['quantity']
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'item_name':product.item_name,
                    'item_price': product.item_price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'getTotal':total
            }
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order, 'cartItems':cartItems}


def cartData(request):
    if request.user.is_authenticated:

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    return {'items':items, 'order':order, 'cartItems':cartItems}


def guestOrder(request, data):
    print(request.COOKIES)
    name = data['userFormInfo']['name']
    email = data['userFormInfo']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    # order = cookieData['order']
    # cartItems = cookieData['cartItems']

    customer, created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        completed=False
    )

    for item in items:

        product = Product.objects.get(id = item['product']['id'])

        orderitem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return customer, order

def send_sms(otp, phonenumber):
    print("Sindhura otp and phonenumber {} {}".format(otp, phonenumber))
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    account_sid = 'AC6c0b660543f1bcc4744ff3dca155b6e1'
    auth_token = '2e3b556d08bcbc5e62c476639dbb59c2'
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(body=f'Hi, your verification code is {otp}',
                                    from_='+14088377119',
                                    to=f'{phonenumber}')
