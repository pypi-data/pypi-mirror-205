from flask_restx import Api
from loguru import logger
from flask import Flask

api = Api()


def init_app(app: Flask):
    logger.info('Inicializando API')
    api.init_app(app)
    return api
