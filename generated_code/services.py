from models import Product, User, Order
from repositories import ProductRepository, UserRepository, OrderRepository

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def get_all_products(self):
        return self.product_repository.get_all()

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_data):
        user = User(
            id=None,  # ID will be generated automatically
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        return self.user_repository.create(user)

    def login_user(self, user_data):
        # Implement user authentication logic here
        # ...
        return "token" # Replace with actual token generation

    def add_to_cart(self, user_id, product_id):
        # Implement cart management logic here
        # ...
        pass  

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()

    def create_order(self, user_id, order_items):
        order = Order(user_id=user_id, order_items=order_items)
        return self.order_repository.create(order)