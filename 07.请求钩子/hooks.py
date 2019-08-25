from flask import Flask

app = Flask(__name__)


# 在第一次请求之前调用，可以在此方法内部做一些初始化操作
@app.before_first_request
def initial():
    print('第一次请求')


# 在每一次请求之前调用，这时候已经有请求了，可能在这个方法里面做请求的校验
# 如果请求的校验不成功，可以直接在此方法中进行响应，直接return之后那么就不会执行视图函数
@app.before_request
def prepare():
    print('请求之前')


# 在执行完视图函数之后会调用，并且会把视图函数所生成的响应传入,可以在此方法中对响应做最后一步统一的处理
@app.after_request
def after(response):  # （如果没有抛出异常）接收视图函数返回的参数
    print('请求之后')


# 请每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息
@app.teardown_request
def finally_down(e):
    print('请求收尾，抛出异常 %s' % e)


# teardown_request 每次请求之后都会执行，会接收异常参数


@app.route('/')
def index():
    pass
