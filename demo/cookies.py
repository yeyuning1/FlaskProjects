from flask import Flask, make_response, request, Response

app = Flask(__name__)


@app.route('/index')
def index():
    response = make_response('idnex')
    response.set_cookie('zz1', '123', max_age=86400)
    return response


@app.route('/demo1')
def demo1():
    name = request.cookies.get('name')
    print(name)
    response = make_response('demo1')  # type:Response
    response = response.delete_cookie('name')
    # 删除 cookie 的本质就是 把 cookie 的 max_age 设置为 0.
    response.set_cookie('name', '1', max_age=0)
    return response
