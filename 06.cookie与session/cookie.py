from flask import Flask, make_response, Response

app = Flask(__name__)


@app.route('/cookie')
def set_cookie():
    res = make_response('set_cookie')  # type: Response
    res.set_cookie('username', 'yyn', max_age=3600)
    res.delete_cookie('username')
    return res
