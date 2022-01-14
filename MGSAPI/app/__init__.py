from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.node_controller import api as node_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.lease_controller import api as lease_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='VM Management Solution REST API',
          version='1.0',
          description='REST API Server for VM Management Solution'
      )

api.add_namespace(user_ns, path='/user')
api.add_namespace(node_ns, path='/node')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(lease_ns, path='/lease')
