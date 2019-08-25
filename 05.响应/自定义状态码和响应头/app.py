from flask import Flask, make_response

app = Flask(__name__)


@app.route('/index1')
def index1():
    return '1', 400, {'errmsg': 'error'}


@app.route('/')
def index():
    res = make_response('test')
    res.headers['name'] = 'yyn'
    res.status = '404 not found'
    return res
