from flask_restful import Resource


class FirstResource(Resource):
    def get(self):
        return {'get': 'foo'}

    def post(self):
        return {'post': 'foo'}
