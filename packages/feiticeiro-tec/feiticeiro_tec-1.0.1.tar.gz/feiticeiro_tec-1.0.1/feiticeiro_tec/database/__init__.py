from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from flask import Flask

db = SQLAlchemy()


def init_app(app: Flask):
    logger.info('Iniciando Banco de Dados')
    db.init_app(app)
    from server.database import models
    logger.debug('Tabelas Inicializadas {}'.format(models.__all__))
    return db
