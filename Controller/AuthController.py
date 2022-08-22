from app import api, Resource, request, json, jsonify
from Services.AuthServices import login


# Realizar login
@api.route('/api/login')
class Auth(Resource):
    def post(self):
        # Armazena o json na variável
        json = request.json
        # Armazena os dados necessários nas variáveis
        email = json['email']
        senha = json['password']
        return login(email=email, senha=senha)
