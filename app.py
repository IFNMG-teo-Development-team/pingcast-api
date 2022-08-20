from flask import Flask, request, json, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api
from flask_cors import CORS

# Instâncias para a aplicação, documentação e CORS
app = Flask(__name__)
api = Api(app,default_swagger_filename="PINGCAST", default="Pingcast-API", default_label="Rotas disponíveis")
JWTManager(app)
CORS(app)

#app.config.SWAGGER_UI_OPERATION_ID = True
#app.config.SWAGGER_UI_REQUEST_DURATION = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from configHeroku import *

try:
    heroku()
except:
    local()

db = SQLAlchemy(app)

from Controller.PerfilController import Perfil
from Controller.AuthController import Auth
from Controller.CanalController import Canal
from Controller.PodcastController import Podcast

if __name__ == '__main__':
    app.run(debug=True)
