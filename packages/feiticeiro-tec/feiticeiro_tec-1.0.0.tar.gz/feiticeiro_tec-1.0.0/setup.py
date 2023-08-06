from setuptools import setup


import os


def listar_subpastas(diretorio):
    subpastas = []
    for nome in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome)
        if os.path.isdir(caminho):
            subpastas.append(caminho)
            subpastas.extend(listar_subpastas(caminho))
    return subpastas


with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='feiticeiro_tec',
    version='1.0.0',
    url='https://github.com/feiticeiro-tec/feiticeiro-tec',
    license='BSD3',
    author='Silvio Henrique Cruz Da Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='silviohenriquecruzdasilva@gmail.com',
    keywords='Pacote',
    description=u'Extenção flask para aumento de agilidade no processo de criação de projeto.',
    packages=listar_subpastas('feiticeiro_tec'),
    install_requires=['flask', 'flask-sqlalchemy',
                      'flask-restx', 'loguru', 'python-dotenv']
)
