class Product:
    """Represents a product in the catalog."""

    def __init__(self, id, name, description, price, inventory):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.inventory = inventory


class User:
    """Represents a registered user."""
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    
class Order:
    """Represents an order placed by a user."""
    def __init__(self, user_id, order_items):
        self.user_id = user_id
        self.order_items = order_items