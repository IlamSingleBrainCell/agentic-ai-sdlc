from flask import Flask
from api import app
from models import db
from config import *

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

if __name__ == '__main__':
  app.run(debug=True)