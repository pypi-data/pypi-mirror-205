import os


def write_model(path, name):
    with open(os.path.join(path, name + '.py'), 'w') as f:
        f.write('from server.database.models import db\n')
        f.write('from server.database.models.base import Base\n\n\n')
        f.write('class {}(Base, db.Model):\n'.format(name.capitalize()))
        f.write('\t__tablename__ = \'{}\'\n'.format(name.capitalize()))
