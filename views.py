from flask_jwt_extended import create_access_token, JWTManager,jwt_required
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, SECRET_KEY
from flask import session, request, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from models import Perfil
from app import app, db


jwt = JWTManager(app)
oauth = OAuth(app)

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

# Rota para cadastro de um novo usuário, recebendo apenas requisição POST
@app.route('/cadastrar', methods=["POST", ])
def cadastrar():
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
    if Perfil.query.filter_by(email=email).first():
        return {"mensagem": "Esse email já está sendo utilizado!"}, 409
    elif Perfil.query.filter_by(username=username).first():
        return {"mensagem": "Esse nome de usuário já está sendo utilizado!"}, 409
    
    # Caso contrário continua as etapas do cadastro
    novo_perfil = Perfil(username=username, data_nascimento=data_nascimento, genero=genero, nome=nome, email=email, senha=senha, tipo_conta='gratuita')
    db.session.add(novo_perfil)
    db.session.commit()
  
    return {"mensagem": "Cadastro realizado com sucesso!"}, 201


# Route to login with Github
@app.route('/login', methods=['POST'])
def login():
    # Armazena o json na variável
    json = request.json
    # Armazena os dados necessários nas variáveis
    email = json['email']
    senha = json['password']

    # Consulta no banco uma ocorrência do email
    perfil = Perfil.query.filter_by(email=email, senha=senha).first()

    if perfil:  # Verifica se um usuário foi encontrado
        token_acesso = create_access_token(perfil.username)
        return jsonify({"token": token_acesso}, 200)

    return {"mensagem": "Credenciais incorretas!"}, 204


@app.route("/logout", methods=['POST', 'GET', ])
@jwt_required()
def logout():
    return {"mensagem": "Logout efetuado com sucesso!"}, 200


# Route to login with Github
@app.route('/login/github')
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


