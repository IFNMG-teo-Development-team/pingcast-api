from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager,jwt_required
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, SECRET_KEY
from flask import session, request, url_for, jsonify, json, make_response
from flask.views import MethodView
from authlib.integrations.flask_client import OAuth
from models import Perfil
from app import app, db
from flask_restful import Api, Resource
from marshmallow import Schema

jwt = JWTManager(app)
oauth = OAuth(app)
api = Api(app)

# registro de autenticação
github = oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/healthcheck')
def healthcheck():
    return {"status": "OK"}


# Route to login with Github
@app.route('/login/github', methods=['POST', 'GET'])
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

# Route to login authorization with Github
@app.route('/login/github/authorize')
def github_authorize():
    token = github.authorize_access_token()
    resp = github.get('user').json()
    return {"token": token}

# [início]\----------- Perfil -----------\

#Criar novo perfil (cadastrar)
@app.route("/perfil", methods=["POST"])
def cadastrar():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    else:
        # Armazena o json na variável
        json = request.json
        # Armazena os dados necessários nas variáveis
        username = json['username']
        genero = json['gender']
        data_nascimento = json['birth_date']
        nome = json['name']
        email = json['email']
        senha = json['password']

        # Verifica se já existe uma conta com esse email
        if Perfil.query.filter_by(username=username).first():
            return _corsify_actual_response(jsonify({"mensagem": "Esse nome de usuário já está sendo utilizado!"}, 409))
        elif Perfil.query.filter_by(email=email).first():
            return _corsify_actual_response(jsonify({"mensagem": "Esse email já está sendo utilizado!"}, 409))
            
        # Caso contrário continua as etapas do cadastro
        novo_perfil = Perfil(username=username, data_nascimento=data_nascimento, genero=genero, nome=nome, email=email, senha=senha, tipo_conta='gratuita')
        db.session.add(novo_perfil)
        db.session.commit()
    
        return _corsify_actual_response(jsonify({"mensagem": "Cadastro realizado com sucesso!"}, 201))

# Realizar login
@app.route("/perfil/login", methods=["POST"])
def login():
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "POST":
        # Armazena o json na variável
        json = request.json
        # Armazena os dados necessários nas variáveis
        email = json['email']
        senha = json['password']

        # Consulta no banco uma ocorrência do email
        perfil = Perfil.query.filter_by(email=email, senha=senha).first()

        if perfil:  # Verifica se um usuário foi encontrado
            token_acesso = create_access_token(perfil.id)
            return _corsify_actual_response(jsonify({"token": token_acesso, "status": 200}))

        return _corsify_actual_response(jsonify({"mensagem": "Email ou senha incorretos!", "status": 204}))

# Buscar dados públicos de um perfil pelo id
@app.route("/perfil/<id>", methods=["GET"])
@jwt_required()
def get_perfil(id):
    if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
    elif request.method == "GET":
        perfil = Perfil.query.filter_by(id=id).first()
        if perfil:
            return _corsify_actual_response(jsonify({"perfil" : jsonConverter(PerfilSchema, perfil), "status":200}))
        else:
            return _corsify_actual_response(jsonify({"status": 404,
                    "mensagem": "Perfil não encontrado!"}))
  
# [Final] \----------- Perfil -----------\


         
# ------ Configurações dos cors ------
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response 
#--------------------------------------

# Classes para definição dos campos de retorno de cada tabela
class PerfilSchema(Schema):
    class Meta:
        fields = ("id", "username", "data_nascimento", "interesses", "descricao", "genero", "nome", "tipo_conta")
# ------------------------------------------------------------


# Função que converte objeto da query em JSON
def jsonConverter(schemaClass: object, toConvertObject: object):
    consulta = schemaClass()
    result = consulta.dump(toConvertObject)
    return result