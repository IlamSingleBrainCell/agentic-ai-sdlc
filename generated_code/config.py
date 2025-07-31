import os

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = DATABASE_URL 

# JWT configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# Other configurations as needed