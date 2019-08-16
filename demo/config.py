from flask import Flask

# class DefaultConfig(object):
#     """默认配置"""
#     SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1'
#
#
# class DevelopmentConfig(DefaultConfig):
#     DEBUG = True
#
#
# app = Flask(__name__)
#
# app.config.from_object(DevelopmentConfig)
#
#
# @app.route("/")
# def index():
#     print(app.config['SECRET_KEY'])
#     return "hello world"
app = Flask(__name__)

app.config.from_pyfile('setting.py')


@app.route("/")
def index():
    print(app.config['SECRET_KEY'])
    return "hello world"


if __name__ == '__main__':
    app.run()
