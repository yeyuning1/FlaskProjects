from flask import Flask

from demo.helloworld import MobileConverter

app = Flask(__name__)

app.url_map.converters['mobile'] = MobileConverter


@app.route('/users/<user_id>')
def user_info(user_id):
    pass


@app.route('/index/<int:number>')
def index(number):
    pass
