from flask import Flask, request, json, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api
from flask_cors import CORS
import boto3
import datetime
import os



try:
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRECT_ACCESS_KEY'],
                        region_name="sa-east-1",
                        )
    # Let's use Amazon S3
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                             aws_secret_access_key=os.environ['AWS_SECRECT_ACCESS_KEY'],
                             region_name="sa-east-1",
                             )

except:
    import config

    s3 = boto3.resource('s3',
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRECT_ACCESS_KEY,
                        region_name="sa-east-1",
                        )

    # Let's use Amazon S3
    s3_client = boto3.client('s3',
                             aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=config.AWS_SECRECT_ACCESS_KEY,
                             region_name="sa-east-1",
                             )

# Instâncias para a aplicação, documentação e CORS
app = Flask(__name__)
api = Api(app, default_swagger_filename="PINGCAST", default="Pingcast-API", default_label="Rotas disponíveis")
JWTManager(app)
CORS(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=365)
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
