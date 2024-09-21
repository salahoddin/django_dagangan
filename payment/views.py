from django.shortcuts import render
from . models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse

# Create your views here.

def checkout(request):
    if request.user.is_authenticated:
        try:
            # user with shipping address
            shipping = ShippingAddress.objects.get(user=request.user.id)

            return render(request, 'payment/checkout.html', {'shipping': shipping})
        except ShippingAddress.DoesNotExist:
            # account has no shipping address
            shipping = None
            return render(request, 'payment/checkout.html')

    else: # guest users
        return render(request, 'payment/checkout.html')
    

def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal = request.POST.get('postal')

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + province + '\n' + postal)

        # shopping cart info
        cart = Cart(request)

        total_cost = cart.get_total()

        '''
        Order Variations: 
        1. Account users WITH + WITHOUT shipping info.
        2. Guest users (without an account)
        '''
        if request.user.is_authenticated:
            print('Authenticated User:=====================================================',  request.user)
            order = Order.objects.create(user=request.user, 
                                         full_name=name, 
                                         email=email, 
                                         shipping_address=shipping_address, 
                                         ammount_paid=total_cost)
            
            order_id = order.pk
            
            for item in cart:
                OrderItem.objects.create(order_id=order_id, 
                                         user=request.user,
                                         product=item['product'], 
                                         price=item['price'], 
                                         quantity=item['quantity'])
                                                  
        else:
            order = Order.objects.create(full_name=name, 
                                         email=email, 
                                         shipping_address=shipping_address, 
                                         ammount_paid=total_cost)
            
            order_id = order.pk
            
            for item in cart:
                OrderItem.objects.create(order_id=order_id, 
                                         product=item['product'], 
                                         price=item['price'], 
                                         quantity=item['quantity'])

        return JsonResponse({'order_success': True})          
        

def payment_success(request):
    # if the payment is a success, clear the cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')