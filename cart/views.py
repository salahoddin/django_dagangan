from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    # print('type of cart', type(cart))
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        # product = Product.objects.filter(pk=product_id)
        product = get_object_or_404(Product, id=product_id)

        if product and product_quantity:
            cart.add(product=product, product_quantity=product_quantity) # adding to session

            cart_quantity = cart.__len__() # this is coming from cart class
            return JsonResponse({'quantity': cart_quantity})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    cart = Cart(request)
    product_id = None
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        if product_id:
            print(product_id)
            cart.delete(product_id=product_id) # removing from session
            cart_quantity = cart.__len__() # this is coming from cart class
            cart_total = cart.get_total()

            return JsonResponse({'product_id': product_id, 'quantity': cart_quantity, 'total': cart_total})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
    cart = Cart(request)
    product_id = None
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))

        if product_id:
            cart.update_quantity(product_id=product_id, quantity=quantity)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()

            # get the price in this part
            price = cart.__dict__.get('cart', {}).get(str(product_id), {}).get('price') # found this using vars(cart)


            return JsonResponse({'quantity': cart_quantity, 'total': cart_total, 'price': price})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)
# def cart_update(request):
#     cart = Cart(request)
#     product_id = None
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         quantity = int(request.POST.get('quantity'))

#         if product_id:
#             cart.update_quantity(product_id=product_id, quantity=quantity)
#             cart_quantity = cart.__len__()
#             cart_total = cart.get_total()

#             # get the price in this part
#             price = cart.__dict__.get('cart', {}).get(str(product_id), {}).get('price') # found this using vars(cart)


#             return JsonResponse({'quantity': cart_quantity, 'total': cart_total, 'price': price})
        
#     return JsonResponse({'error': 'Invalid request'}, status=400)
