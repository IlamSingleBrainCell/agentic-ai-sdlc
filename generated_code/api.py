from flask import Flask, request, jsonify
from services.user_service import UserService
from services.product_service import ProductService
from services.order_service import OrderService

app = Flask(__name__)

user_service = UserService()
product_service = ProductService()
order_service = OrderService()


@app.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products from the catalog."""
    products = product_service.get_all_products()
    return jsonify(products)


@app.route('/users/register', methods=['POST'])
def register_user():
    """Register a new user."""
    data = request.get_json()
    user = user_service.create_user(data)
    return jsonify(user), 201


@app.route('/users/login', methods=['POST'])
def login_user():
    """Log in an existing user."""
    data = request.get_json()
    token = user_service.login_user(data)
    return jsonify({'token': token})


@app.route('/cart', methods=['POST'])
def add_to_cart():
    """Add an item to the user's cart."""
    data = request.get_json()
    user_service.add_to_cart(data['user_id'], data['product_id'])
    return jsonify({'message': 'Item added to cart'})