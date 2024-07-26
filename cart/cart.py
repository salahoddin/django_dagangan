class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        # if the user is a new visitor, create a new session
        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart