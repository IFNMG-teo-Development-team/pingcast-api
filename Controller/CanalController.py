from app import api, Resource, request, json
from flask_jwt_extended import jwt_required
from Services.CanalServices import *

@api.route("/api/perfil/<int:id>/canal")
class Canal(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        return getCanalByIdPerfil(id)

    @classmethod
    @jwt_required()
    def post(cls, id):
        canal = json.loads(request.data)
        return addCanal(canal, id)

    @classmethod
    @jwt_required()
    def put(cls, id):
        canal = json.loads(request.data)
        return editCanal(canal, id)

    @classmethod
    def delete(cls, id):
        return deleteCanal(id)
@api.route("/api/canal")
class Canal(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return getCanais()
