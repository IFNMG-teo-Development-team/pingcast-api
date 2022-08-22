from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash
from Models.PerfilModel import Perfil
from flask import abort


def login(email, senha):
    # Consulta no banco uma ocorrência do email
    try:
        perfil = Perfil.query.filter_by(email=email).first()
        if perfil:  # Verifica se um usuário foi encontrado
            if check_password_hash(perfil.senha, senha):
                token_acesso = create_access_token(perfil.id)
                return {"status": 200,
                        "token": token_acesso,
                        "id": perfil.id,
                        "username": perfil.username}

            return {"message": "Incorrect credentials"}, 403

        return {"message": "Incorrect credentials"}, 403

    except:
        return abort(500, "There was an error during authentication")
