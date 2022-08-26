from app import api, Resource, request, json
from Services.PodcastServices import *
from flask_jwt_extended import jwt_required


@api.route("/api/perfil/<int:id_perfil>/canal/podcast/<int:id_podcast>")
class Canal(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id_perfil, id_podcast):
        return getPodcastByIds(id_podcast, id_perfil)

    @classmethod
    @jwt_required()
    def delete(cls, id_perfil, id_podcast):
        return deletePodcast(id_podcast, id_perfil)

    @classmethod
    @jwt_required()
    def put(cls, id_perfil, id_podcast):
        podcast = json.loads(request.data)
        return editPodcast(id_podcast, id_perfil, podcast)


@api.route("/api/perfil/<int:id_perfil>/canal/podcast")
class Canal(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id_perfil):
        return getCanalPodcastById(id_perfil)

    @classmethod
    @jwt_required()
    def post(cls, id_perfil):
        podcast = json.loads(request.form.get('info'))
        audio = request.files["audio"].read()
        return addPodcast(podcast, id_perfil, audio)


@api.route("/api/podcast")
class Canal(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return getAllPodcasts()
