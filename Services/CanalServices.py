from flask import session, request, url_for, jsonify, json, make_response, abort
from flask_restx import fields, marshal_with
from app import db
from Models.CanalModel import *
from Models.PerfilModel import *

# Campos para serialização dos dados
resource_fields = {
    "id": fields.Integer,
    "nome": fields.String,
    "bio": fields.String,
    "tema": fields.String,
    "dono": fields.Integer,
}


@marshal_with(resource_fields)
def getCanalByIdPerfil(id_perfil):
    canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
    return canal


def addCanal(canal, id_perfil):
    perfil = Perfil.query.filter_by(id=id_perfil).first()
    if perfil:
        canal_unico = Canal.query.filter_by(dono=id_perfil).first()
        if canal_unico:
            return abort(409, "This user already has a channel")
        else:
            try:
                novo_canal = Canal(nome=canal['nome'], bio=canal['bio'], tema=canal['tema'], dono=id_perfil)
                db.session.add(novo_canal)
                db.session.commit()
                return {"message": "The channel was successfully created"}, 201
            except:
                return abort(500, "There was an error when creating the channel")
    else:
        return abort(404, "Profile not found")


def deleteCanal(id_perfil):
    try:
        canal = Canal.query.filter_by(dono=id_perfil).first()
        if canal:
            db.session.delete(canal)
            db.session.commit()
            return {"message": "The channel was successfully deleted"}, 201
        else:
            return abort(404)
    except:
        return abort(500)


def editCanal(canal_dados, id_perfil):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
    try:
        canal.nome = canal_dados['nome']
        canal.bio = canal_dados['bio']
        canal.tema = canal_dados['tema']
        db.session.add(canal)
        db.session.commit()
        return {"message": "The channel was successfully edited"}, 201
    except:
        return abort(500, "There was an error when editing the channel")


@marshal_with(resource_fields)
def getCanais():
    canal = Canal.query.all()
    return canal
