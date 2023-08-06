from flask_restx import Resource
from server.api import api

np_usuario = api.namespace('usuario', description='Operações relacionadas a usuários')


class UsuarioResource(Resource):
    ...