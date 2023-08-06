import sys
import os
import shutil
from .create.model import write_model
from .create.namespace import write_namespace

path_file, command = sys.argv[0], sys.argv[1]
root = sys.path[0]


def create_tree(root):
    os.makedirs(os.path.join(root, 'server'))
    shutil.copytree(os.path.join(os.path.dirname(__file__),
                    'api'), os.path.join(root, 'server', 'api'))
    shutil.copytree(os.path.join(os.path.dirname(__file__),
                    'database'), os.path.join(root, 'server', 'database'))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'create',
                    'server.py'), os.path.join(root, 'server', '__init__.py'))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'create',
                    'app.py'), os.path.join(root, 'app.py'))
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'create', 'env.py'),
                    os.path.join(root, '.env'))


def create_namespace_on_version(version, name, model, is_create_model):
    path = os.path.join(root, 'server', 'api', version, name)
    os.makedirs(path)
    write_namespace(os.path.join(root, 'server', 'api',
                    version, name), name)
    if is_create_model:
        write_model(os.path.join(root, 'server',
                    'database', 'models'), model)


if command == 'create_server':
    create_tree(root=root)

elif command == 'create_namespace':
    version = input('Qual a Versão? ')
    namespace = input('Qual o Nome Do NameSpace? ')
    is_create_model = input('Deseja Criar o Model? (S/n) ').upper()
    if is_create_model == '' or is_create_model == 'S':
        is_create_model = True
        model = input('Qual o Nome Do Model? ')
    else:
        is_create_model = False
        model = None

    create_namespace_on_version(version, namespace, model, is_create_model)
