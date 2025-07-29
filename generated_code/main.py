from flask import Flask
from api import app
from services import search_stock

if __name__ == '__main__':
    app.run(debug=True)