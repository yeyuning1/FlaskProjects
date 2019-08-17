# 导入Flask类
from flask import Flask, make_response, Response

# Flask类接收一个参数__name__
from werkzeug.routing import BaseConverter

app = Flask(__name__,
            static_url_path='/url_path_param',  # 静态文件url访问资源路径
            static_folder='folder_param')  # 静态文件目录


# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return 'Hello World'


class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}$'


app.url_map.converters['mob'] = MobileConverter


@app.route('/user/<mob:mobile>')
def mobile(mobile):
    response = make_response(mobile)  # type: Response
    response.headers['b'] = '123'
    response = response.set_cookie('zzz', '123', expires=300)
    return response


# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    app.run()
