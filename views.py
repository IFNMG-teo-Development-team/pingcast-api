from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required
from flask import session, request, url_for, jsonify, json, make_response
from flask.views import MethodView
from authlib.integrations.flask_client import OAuth
from models import Perfil
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from serializers import PerfilSerializer
import os.path
import secrets
from flask_cors import cross_origin
from flask_cors import CORS

jwt = JWTManager(app)
oauth = OAuth(app)
api = Api(app)
CORS(app)
# Registro de autenticação github e google
try:
    from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

    github = oauth.register(
        name='github',
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user'},
    )

    google = oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )

except:
    github = oauth.register(
        name='github',
        client_id=os.environ['GITHUB_CLIENT_ID'],
        client_secret=os.environ['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    google = oauth.register(
        name='google',
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )


@app.route('/healthcheck')
def healthcheck():
    return {"status": "OK"}


# Route to login with Github
@app.route('/login/github', methods=['POST', 'GET', 'OPTIONS'])
def github_login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    else:
        github = oauth.create_client('github')
        redirect_uri = url_for('github_authorize', _external=True)
        return _corsify_actual_response(github.authorize_redirect(redirect_uri))


# Route to login authorization with Github

@app.route('/login/github/authorize', methods=['GET', 'POST', 'OPTIONS'])
def github_authorize():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    else:

        token = github.authorize_access_token()

        resp = github.get('user').json()

        # Verifica se já está cadastrado
        if Perfil.query.filter_by(social_id=resp['id']).first():
            perfil = Perfil.query.filter_by(username=resp['login']).first()
            token_acesso = create_access_token(perfil.id)
            return _corsify_actual_response(jsonify({"status": 200,
                                                     "token": token_acesso,
                                                     "id": perfil.id,
                                                     "username": perfil.username}))
        # Verifica se já existe um usuário com esse username (Isso vai ter um problema para corrigir)
        elif Perfil.query.filter_by(username=resp['login']).first():
            return _corsify_actual_response(
                jsonify({"mensagem": "Esse nome de usuário já está sendo utilizado!"}, 409))
        else:
            try:
                # Realiza o cadastro do novo usuário pelo github
                cadastrar_github(resp)
                perfil = Perfil.query.filter_by(username=resp['login']).first()
                token_acesso = create_access_token(perfil.id)
                return _corsify_actual_response(jsonify({"status": 200,
                                                         "token": token_acesso,
                                                         "id": perfil.id,
                                                         "username": perfil.username}))
            except:
                return _corsify_actual_response(jsonify({'Mensagem': 'Erro ao conectar!'}))


# Route to login with Google
@app.route('/login/google', methods=['POST', 'GET'])
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# Route to login authorization with Google
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    return _corsify_actual_response(jsonify({"status": token}))


# Criar novo perfil github(cadastrar)
def cadastrar_github(json):
    # Armazena os dados necessários nas variáveis
    username = json['login']
    nome = json['name']
    email = secrets.token_hex(nbytes=16)  # Valor aleatório para preencher o campo
    senha = secrets.token_hex(nbytes=16)  # Valor aleatório para preencher o campo
    social_id = json['id']

    # Etapas do cadastro
    novo_perfil = Perfil(username=username, nome=nome,
                         email=email, senha=senha, tipo_conta='gratuita', social_id=social_id)
    db.session.add(novo_perfil)
    db.session.commit()


# [início]\----------- Perfil -----------\

# Criar novo perfil (cadastrar)
@app.route("/api/perfil", methods=["POST"])
def cadastrar():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        # Armazena o json na variável
        json = request.json
        # Armazena os dados necessários nas variáveis
        try:
            username = json['username']
            genero = json['sexo']
            data_nascimento = json['birth']
            sobrenome = json['sobrenome']
            nome = json['nome']
            email = json['email']
            senha = json['senha']
            senha = generate_password_hash(senha, "sha256")
        except Exception as e:
            return _corsify_actual_response(
                jsonify({"mensagem": "Informeções faltando, verifique os parametros informados!"}, e))

        try:
            # Verifica se já existe uma conta com esse email
            if Perfil.query.filter_by(username=username).first():
                return _corsify_actual_response(
                    jsonify({"mensagem": "Esse nome de usuário já está sendo utilizado!"}, 409))
            elif Perfil.query.filter_by(email=email).first():
                return _corsify_actual_response(jsonify({"mensagem": "Esse email já está sendo utilizado!"}, 409))

            # Caso contrário continua as etapas do cadastro
            novo_perfil = Perfil(username=username, data_nascimento=data_nascimento, genero=genero, nome=nome,
                                 email=email, senha=senha, tipo_conta='gratuita', sobrenome=sobrenome)
            db.session.add(novo_perfil)
            db.session.commit()

            return _corsify_actual_response(jsonify({"mensagem": "Cadastro realizado com sucesso!", "status": 201}))
        except Exception as e:
            return _corsify_actual_response(jsonify({"mensagem": e}))


# Realizar login
@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":
        # Armazena o json na variável
        json = request.json
        # Armazena os dados necessários nas variáveis
        email = json['email']
        senha = json['password']

        # Consulta no banco uma ocorrência do email
        try:
            perfil = Perfil.query.filter_by(email=email).first()

            if perfil:  # Verifica se um usuário foi encontrado

                if check_password_hash(perfil.senha, senha):
                    token_acesso = create_access_token(perfil.id)
                    return _corsify_actual_response(jsonify({"status": 200,
                                                             "token": token_acesso,
                                                             "id": perfil.id,
                                                             "username": perfil.username}))

                return _corsify_actual_response(jsonify({"mensagem": "Email ou senha incorretos!", "status": 204}))
            return _corsify_actual_response(jsonify({"mensagem": "Email ou senha incorretos!", "status": 204}))

        except:
            return _corsify_actual_response(jsonify({"Mensagem": "Houve um problema ao conectar ao banco"}))


# Buscar dados públicos de um perfil pelo id
@app.route("/api/perfil/<id>", methods=["GET"])
@jwt_required()
def get_perfil(id):
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "GET":
        try:
            perfil = Perfil.query.filter_by(id=id).first()
            if perfil:
                return _corsify_actual_response(
                    jsonify({"perfil": jsonConverter(PerfilSerializer, perfil), "status": 200}))
            else:
                return _corsify_actual_response(jsonify({"status": 404,
                                                         "mensagem": "Perfil não encontrado!"}))
        except:
            return _corsify_actual_response(jsonify({"Mensagem": "Houve um problema ao conectar ao banco"}))


# Consulta todos os perfis cadastrados (dados públicos)
@app.route("/api/perfil", methods=["GET"])
@jwt_required()
def get_perfis():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "GET":

        perfil = Perfil.query.all()

        lista_perfis = []

        # Faz iteração para realizar uma lista de dicionarios para cada perfil
        for i in range(0, len(perfil)):
            lista_perfis.append({f"{i}": jsonConverter(PerfilSerializer, perfil[i])})

        if perfil:
            return _corsify_actual_response(jsonify({"Perfis": lista_perfis}))
        else:
            return _corsify_actual_response(jsonify({
                "status": 404,
                "mensagem": "Nenhum perfil encontrado!"}))


# Realiza deleção do perfil logado
@app.route("/api/perfil", methods=["DELETE"])
@jwt_required()
def delete_perfil():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "DELETE":
        try:
            id = get_jwt_identity()
            print(id)
            try:
                perfil = Perfil.query.filter_by(id=id).first()
                db.session.delete(perfil)
                db.session.commit()
                return _corsify_actual_response(
                    jsonify({"Mensagem": "Perfil deletado com sucesso", "status": 200}))
            except:
                return _corsify_actual_response(jsonify({"status": 200,
                                                         "mensagem": "Houve um problema ao tentar deletar o perfil!"}))
        except:
            return _corsify_actual_response(jsonify({"Mensagem": "Houve um problema ao conectar ao banco"}))


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


# ------------------------------------------------------------


# Função que converte objeto da query em JSON
def jsonConverter(schemaClass: object, toConvertObject: object):
    consulta = schemaClass()
    result = consulta.dump(toConvertObject)
    return result
