from flask import Flask, session

app = Flask(__name__)


class DefaultConfig(object):
    # base64.encode(os.urandom(40)).decode()
    SECRET_KEY = 'nrNi3405iiJrt2ztyHn/o+ggkEzzX0fNgEWjxW8GWBxPLz4x+jHzDQ=='


# app.secret_key='test'
app.config.from_object(DefaultConfig)


# 这里的session数据保存到了cookie中 且仅使用了b64编码
@app.route('/')
def index():
    session['username'] = 'yyn'
    # session.get('username')
    return 'ok'
