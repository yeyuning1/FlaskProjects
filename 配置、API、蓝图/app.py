from flask import Flask

from config import config_dict
from home import home_blu


def index():
    pass


def create_app(config_type):
    app = Flask(__name__)
    config_class = config_dict.get(config_type)
    app.config.from_object(config_class)
    app.config.from_envvar('MY_ENV', silent=True)
    app.add_url_rule('/', endpoint='index', view_func=index)
    app.register_blueprint(home_blu)
    return app


"""
$ export FLASK_APP="app:create_app('dev')"
$ export FLASK_ENV=development
$ flask run
"""
