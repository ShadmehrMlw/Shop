CART_SESSIONS_ID = 'cart'

class Cart:
    def __int__(self, request):
        self.sessions = request.sessions
        cart = self.sessions.get(CART_SESSIONS_ID)
        if not cart:
            cart = self.sessions[CART_SESSIONS_ID] = {}
        self.cart = cart