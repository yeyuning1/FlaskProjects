import base64
import os
from datetime import timedelta

from flask import Flask, session

app = Flask(__name__)
# 使用session需要设置 app 密钥
# base64.b64encode(os.urandom(40)).decode()
app.secret_key = 'FqvX/9HJLcOyjLGyjGucNCgkMJYBnC3QaAMpfJgceKFFwlChECuksw=='
app.permanent_session_lifetime = timedelta(days=7)


@app.route('/index')
def index():
    # 设置session支持过期时间 默认不支持
    session.permanent = True
    # 记录session数据
    session['name'] = 'zs'
    # 删除session数据
    session.pop('name')
    return 'index'


@app.route('/get_session')
def get_session():
    # 获取session数据
    name = session.get('name')
    return name


if __name__ == '__main__':
    app.run(debug=True)
