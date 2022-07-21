from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os.path

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.path.exists('config.py'):
    from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
else:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['SQLALCHEMY_DATABASE_URI']

app.config["JWT_SECRET_KEY"] = SECRET_KEY

db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run()
