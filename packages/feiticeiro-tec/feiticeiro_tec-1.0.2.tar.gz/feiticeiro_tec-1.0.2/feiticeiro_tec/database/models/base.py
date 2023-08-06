from server.database.models import db
from sqlalchemy import Column, DateTime, Boolean, String
from datetime import datetime
import uuid
from loguru import logger


class Base():
    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_delete = Column(Boolean, default=False)

    def add(self):
        logger.debug('Adicionando {} ao Banco de Dados'.format(self))
        db.session.add(self)

    def save(self):
        logger.debug('Salvando {} no Banco de Dados'.format(self))
        db.session.commit()

    def delete(self):
        logger.debug('Deletando {} do Banco de Dados'.format(self))
        self.is_delete = True
        self.save()

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.id)
