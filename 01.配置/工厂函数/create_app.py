from flask import Flask


def create_app(config_type, custom_config=None):
    app = Flask(__name__)
    from .config import config_map
    current_config = config_map[config_type]
    app.config.from_object(current_config)
    # app.config.from_envvar('ENV_CONFIG', silent=True)
    if custom_config:
        app.config.from_envvar(custom_config)
    return app
