# 导入Flask类
from flask import Flask

# Flask类接收一个参数__name__
app = Flask(__name__,
            static_url_path='/url_path_param',  # 静态文件url访问资源路径
            static_folder='folder_param')  # 静态文件目录
app.config

# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return 'Hello World'


# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    app.run()
