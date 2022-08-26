from flask import session, request, url_for, jsonify, json, make_response, abort
from flask_restx import fields, marshal_with
from Models.PodcastModel import Podcast
from Models.PerfilModel import Perfil
from Models.CanalModel import Canal
from Services.AWSServices import *
from app import db
from datetime import datetime
from mutagen.mp3 import MP3

# Campos para serialização dos dados
resource_fields = {
    "id": fields.Integer,
    "duracao": fields.String,
    "data_postagem": fields.String,
    "participantes": fields.String,
    "nome": fields.String,
    "descricao": fields.String,
    "post_podcast": fields.Integer,
    "url": fields.String,
}

@marshal_with(resource_fields)
def getPodcastByIds(id_podcast, id_perfil):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    if perfil:
        canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
        if canal:
            podcast = Podcast.query.filter_by(id=id_podcast, post_podcast=canal.id).first_or_404()
            nome = f"{perfil.id}_{podcast.id}.mp3"
            link = getFileBucket(nome)
            return {
                "id": podcast.id,
                "duracao": podcast.duracao,
                "data_postagem": podcast.data_postagem,
                "participantes": podcast.participantes,
                "nome": podcast.nome,
                "descricao": podcast.descricao,
                "post_podcast": podcast.post_podcast,
                "url": link,
            }


@marshal_with(resource_fields)
def getPodcast(id):
    podcast = Podcast.query.filter_by(id=id).first_or_404()

    canal = Canal.query.filter_by(id=podcast.post_podcast).first_or_404()

    perfil = Perfil.query.filter_by(id=canal.dono).first_or_404()

    nome = f"{perfil.id}_{podcast.id}.mp3"
    link = getFileBucket(nome)

    return {
        "id": podcast.id,
        "duracao": podcast.duracao,
        "data_postagem": podcast.data_postagem,
        "participantes": podcast.participantes,
        "nome": podcast.nome,
        "descricao": podcast.descricao,
        "post_podcast": podcast.post_podcast,
        "url": link,
    }


@marshal_with(resource_fields)
def getAllPodcasts():
    podcasts = Podcast.query.all()
    return podcasts


def deletePodcast(id_podcast, id_perfil):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    if perfil:
        canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
        if canal:
            podcast = Podcast.query.filter_by(id=id_podcast, post_podcast=canal.id).first_or_404()
            if podcast:
                db.session.delete(podcast)
                db.session.commit()

                deleteFileBucket(f'{perfil.id}_{podcast.id}.mp3')

                return {"message": "The podcast was successfully deleted"}, 201


def addPodcast(descricao, nome, participantes, id_perfil, file):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    canal = Canal.query.filter_by(dono=id_perfil).first_or_404()

    audio = MP3(file)
    tamanho = audio.info.length
    try:
        novo_podcast = Podcast(nome=nome, descricao=descricao,
                               duracao=tamanho,
                               participantes=participantes,
                               data_postagem=datetime.today().strftime('%Y-%m-%d'),
                               post_podcast=canal.id)
        db.session.add(novo_podcast)
        db.session.commit()
        # filename = Path(f'{perfil.id}_{novo_podcast.id}.mp3')

        # filename.write_bytes(file)
        #setFileBucket(file, perfil.id, novo_podcast.id)

        return {"message": "Podcast was created successfully"}, 201
    except:
        return abort(500, "There was an error when creating the podcast")


def editPodcast(id_podcast, id_perfil, pod):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    if perfil:
        canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
        if canal:
            podcast = Podcast.query.filter_by(id=id_podcast, post_podcast=canal.id).first_or_404()
            try:
                podcast.participantes = pod['participantes']
                podcast.nome = pod['nome']
                podcast.descricao = pod['descricao']
                db.session.add(podcast)
                db.session.commit()

                return {"message": "Podcast was edited successfully"}, 200
            except:
                return abort(500, "There was an error when editing the podcast")

    else:
        return abort(404, "Profile not found")


@marshal_with(resource_fields)
def getCanalPodcastById(id_perfil):
    perfil = Perfil.query.filter_by(id=id_perfil).first_or_404()
    if perfil:
        canal = Canal.query.filter_by(dono=id_perfil).first_or_404()
        if canal:
            podcasts = Podcast.query.filter_by(post_podcast=canal.id).all()
            return podcasts
