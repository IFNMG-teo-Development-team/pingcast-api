from Services.PerfilServices import *
from app import api, Resource, request, json
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required

@api.route('/api/perfil')
class PerfilController(Resource):
    @classmethod
    @jwt_required()
    @api.doc(summary='get_something')
    def get(cls):
        return getPerfis()

    @classmethod
    def post(cls):
        perfil = json.loads(request.data)
        return addPerfil(perfil)

@api.route('/api/perfil/<int:id>')
class PerfilController(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        return getPerfilById(id)

    @classmethod
    @jwt_required()
    def delete(cls, id):
        deletePerfil(id)
        return {"message": "Profile was successfully deleted"}

