import re

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from home.utils import decorator1, decorator2


class FirstResource(Resource):
    method_decorators = {
        'get': decorator1,
        'post': decorator2
    }

    def get(self, func1=lambda x: x if re.match('^user:.*?', x) else None):
        parser = RequestParser()
        parser.add_argument(name='name',
                            required=False,
                            help='不符合格式',
                            action='store',  # append
                            type=func1,
                            location='args',  # form/json/data/files/headers
                            ignore=False,
                            case_sensitive=False,
                            trim=True,
                            nullable=True)
        parser.add_argument('age')
        args = parser.parse_args()
        name = args.name
        age = args.age
        return {'get': 'foo'}

    def post(self):
        return {'post': 'foo'}
