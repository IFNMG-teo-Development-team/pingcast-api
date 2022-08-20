import os.path
from app import app


def heroku():
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']


def local():
    import config
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["JWT_SECRET_KEY"] = config.SECRET_KEY
