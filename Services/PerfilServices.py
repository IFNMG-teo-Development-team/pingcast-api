from werkzeug.security import generate_password_hash
from Models.PerfilModel import Perfil, db
from flask_restx import fields, marshal_with
from flask import abort

from Services.AuthServices import login

# Campos para serialização dos dados
resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "data_nascimento": fields.String,
    "interesses": fields.String,
    "descricao": fields.String,
    "genero": fields.String,
    "nome": fields.String,
    "sobrenome": fields.String,
    "tipo_conta": fields.String,
}


@marshal_with(resource_fields)
def getPerfis():
    perfil = Perfil.query.all()
    return perfil


@marshal_with(resource_fields)
def getPerfilById(perfil_id):
    perfil = Perfil.query.filter_by(id=perfil_id).first()
    if perfil:
        return perfil
    else:
        return abort(404)


def addPerfil(perfil):
    newpassword = generate_password_hash(perfil['senha'], "sha256")

    if Perfil.query.filter_by(username=perfil["username"]).first():
        return abort(409, "Username is already in use")
    elif Perfil.query.filter_by(email=perfil["email"]).first():
        return abort(409, "E-mail is already in use")
    else:
        try:
            novo_perfil = Perfil(username=perfil['username'], genero=perfil["sexo"], data_nascimento=perfil["birth"],
                                 sobrenome=perfil["sobrenome"], nome=perfil["nome"], email=perfil["email"],
                                 senha=newpassword, tipo_conta="0")
            db.session.add(novo_perfil)
            db.session.commit()

            return login(email=perfil['email'], senha=perfil['senha'])
        except:
            return abort(500, "There was an error during registration")


def deletePerfil(id_perfil):
    try:
        perfil = Perfil.query.filter_by(id=id_perfil).first()
        db.session.delete(perfil)
        db.session.commit()
    except:
        return abort(500)
