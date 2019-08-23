# 导入Flask类
from flask import Flask, make_response, Response, url_for, request

# Flask类接收一个参数__name__
from flask.json import jsonify
from werkzeug.routing import BaseConverter

app = Flask(__name__,
            static_url_path='/url_path_param',  # 静态文件url访问资源路径
            static_folder='folder_param')  # 静态文件目录


# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return 'Hello World'


# 格式转换器
class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}$'


app.url_map.converters['mob'] = MobileConverter


# 路径匹配参数
@app.route('/user/<mob:mobile>')
def mobile(mobile):
    response = make_response(mobile)  # type: Response
    # 自定义响应对象
    response.headers['b'] = '123'
    response = response.set_cookie('zzz', '123', max_age=300)
    return response


# Json格式转换
@app.route('/json')
def json():
    data = {'age': 10, 'name': '123'}
    return jsonify(data)  # 自动转化类字典为json格式，并且将响应头中的 Content_Type 转换为 Application/Json


# 重定向
@app.route('/redirect')
def redirect():
    # 修改 heards 中的Location
    # 修改 Status Code 为 30X
    # return redirect('http://www.baidu.com')

    # 重定向到自己的网页 直接写资源段
    # return redirect('/')

    # 获取视图函数的 url 资源段
    # 获取动态url的时候 需要指定对应参数的值
    url = url_for('mobile', mobile=10)
    return redirect(url)


# 自定义状态码
@app.route('/code')
def code():
    # return 响应体, 状态码, 响应头{}
    return 'code', 666, {'c': 30}


# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    app.run()  # 1.0 以后推荐使用命令行 flask run 来运行程序, 需要提前配置 FLASK_ENV 或者 FLASK_DEBUG=1
