import re

from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from home.utils import decorator1, decorator2


def func1(value):
    if re.match(r'^1[3-9]\d{9}$', value):
        return value
    else:
        raise ValueError('格式不匹配')


class FirstResource(Resource):
    method_decorators = {
        'get': decorator1,
        'post': decorator2
    }

    def get(self):
        parser = RequestParser()
        parser.add_argument(name='name',
                            dest='username',
                            required=False,
                            help='不符合格式',
                            action='store',  # append
                            type=inputs.regex('xx'),
                            location='args',  # form/json/data/files/headers
                            ignore=False,
                            case_sensitive=False,
                            trim=True,
                            nullable=True)
        parser.add_argument('age', type=func1)
        args = parser.parse_args()
        name = args.username
        age = args.age
        return {'get': 'foo'}

    def post(self):
        return {'post': 'foo'}
