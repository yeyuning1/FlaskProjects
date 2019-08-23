from flask import Flask, abort

app = Flask(__name__)


# flask中对于http错误封装了异常处理 可以捕获异常, 亦可以主动抛出异常
@app.route('/index')
def index():
    # num = 1 / 0
    # 主动抛出http错误 只能抛出http错误
    abort(404)
    return 'index'


# 捕获http错误
@app.errorhandler(404)
def not_found(e):
    print(e)
    return e


# 捕获系统内置的错误
@app.errorhandler(ZeroDivisionError)
def division_error(e):
    print(e)
    return e


if __name__ == '__main__':
    app.run(debug=True)
