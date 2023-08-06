class price:

    def calculate_price(self, weight, base_price=10.99):
        if weight < 1:
            return base_price
        else:
            price = base_price * weight
            return price