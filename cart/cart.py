from decimal import Decimal
from store.models import Product
import copy
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        # if the user is a new visitor, create a new session
        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart
    
    def add(self, product, product_quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            # self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] + product_quantity
            self.cart[product_id]['quantity'] = product_quantity
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': product_quantity}

        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    # def update_quantity(self, product_id, quantity):
    #     product_id = str(product_id)
    #     if product_id in self.cart:
    #         self.cart[product_id]['quantity'] = quantity

    #     self.session.modified = True

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity

        self.session.modified = True
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price']) 

            item['total'] = item['price'] * item['quantity']

            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())