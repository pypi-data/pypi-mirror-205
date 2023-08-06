import os


def write_namespace(path, name):
    cap_name = name.capitalize()
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write('from flask_restx import Resource\n')
        f.write('from server.api import api\n\n\n')
        f.write('np_{} = api.namespace(\'{}\')\n\n\n'.format(name, name))
        f.write('class {}Resource(Resource):\n'.format(cap_name))
        f.write('\tdef post(self):\n')
        f.write('\t\tpass\n\n')
        f.write('\tdef get(self, id=None):\n')
        f.write('\t\tpass\n\n')
        f.write('\tdef patch(self, id):\n')
        f.write('\t\tpass\n\n')
        f.write('\tdef delete(self, id):\n')
        f.write('\t\tpass\n\n\n')
        f.write(
            (
                'np_{}.add_resource({}Resource,'
                ' \'/<string:id>\', methods=["GET","POST"])\n'
            ).format(name, cap_name))
        f.write(
            (
                'np_{}.add_resource({}Resource, \'/\','
                'methods=["GET","PATCH","DELETE"])\n'
            ).format(name, cap_name))
