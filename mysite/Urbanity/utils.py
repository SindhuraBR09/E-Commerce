from . models import *
import json

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
