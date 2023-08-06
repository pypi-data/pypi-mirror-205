from flask import Flask
from server.api import init_app as ini_api
from server.database import init_app as ini_database
from loguru import logger
from flask_alembic import Alembic


class Servidor(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config.from_prefixed_env()

    def init_api(self):
        self.api = ini_api(self)

    def init_database(self):
        self.db = ini_database(self)

    def init_commands(self):
        @self.cli.command()
        def migrate_db():
            logger.info('Migrando Banco de Dados')
            alembic = Alembic()
            alembic.revision('autogenerate')
            alembic.upgrade('head')

        @self.cli.command()
        def create_db():
            logger.info('Criando Banco de Dados')
            with self.app_context():
                self.db.create_all()
