class User:
    """Represents a user in the system."""
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

class Booking:
    """Represents a booking in the system."""
    def __init__(self, booking_id, user_id, date, status):
        self.booking_id = booking_id
        self.user_id = user_id
        self.date = date
        self.status = status