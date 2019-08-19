from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from home.utils import decorator1, decorator2


class FirstResource(Resource):
    method_decorators = {
        'get': decorator1,
        'post': decorator2
    }

    def get(self):
        parser = RequestParser()
        parser.add_argument('name')
        parser.add_argument('age')
        args = parser.parse_args()
        args.name
        args.age
        return {'get': 'foo'}

    def post(self):
        return {'post': 'foo'}
