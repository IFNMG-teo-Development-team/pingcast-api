from app import api, Resource, request, json
from flask_jwt_extended import jwt_required
from Services.CanalServices import *

@jwt_required()
@api.route("/api/perfil/<int:id>/canal")
class Canal(Resource):
    @classmethod
    def get(cls, id):
        return getCanalByIdPerfil(id)

    @classmethod
    def post(cls, id):
        canal = json.loads(request.data)
        return addCanal(canal, id)


    @classmethod
    def delete(cls, id):
        return deleteCanal(id)

@jwt_required()
@api.route("/api/canal")
class Canal(Resource):
    @classmethod
    def get(cls):
        return getCanais()
