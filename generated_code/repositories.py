class ProductRepository:
    def __init__(self):
        self.products = [
            Product(1, "Laptop", "Powerful laptop for work and play", 1200, 10),
            Product(2, "Mouse", "Ergonomic wireless mouse", 25, 50),
            # ... add more products
        ]

    def get_all(self):
        return self.products

class UserRepository:
    def __init__(self):
        self.users = []

    def create(self, user):
        self.users.append(user)
        return user

class OrderRepository:
    def __init__(self):
        self.orders = []

    def create(self, order):
        self.orders.append(order)
        return order