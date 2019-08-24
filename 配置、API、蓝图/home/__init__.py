from flask import Blueprint
from flask_restful import Api

from home.views import FirstResource

home_blu = Blueprint('home_b', __name__, url_prefix='/home')

home_api = Api(home_blu)

home_api.add_resource(FirstResource, 'first')
