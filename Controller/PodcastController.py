from app import api, Resource, request, json
from Services.PodcastServices import *
from flask_jwt_extended import jwt_required


@jwt_required()
@api.route("/api/perfil/<int:id_perfil>/canal/podcast/<int:id_podcast>")
class Canal(Resource):
    @classmethod
    def get(cls, id_perfil, id_podcast):
        return getPodcastByIds(id_podcast, id_perfil)

    @classmethod
    def delete(cls, id_perfil, id_podcast):
        return deletePodcast(id_podcast, id_perfil)


@jwt_required()
@api.route("/api/perfil/<int:id_perfil>/canal/podcast")
class Canal(Resource):
    @classmethod
    def get(cls, id_perfil):
        return getCanalPodcastById(id_perfil)

    @classmethod
    def post(cls, id_perfil):
        podcast = json.loads(request.data)
        return addPodcast(podcast, id_perfil)


@jwt_required()
@api.route("/api/podcast")
class Canal(Resource):
    @classmethod
    def get(cls):
        return getAllPodcasts()
