from flask import Flask, request
from werkzeug.datastructures import MultiDict, EnvironHeaders

app = Flask(__name__)


@app.route('/')
def index():
    # data 记录请求的数据，转换为字符换
    request.data
    # form 记录表单的数据
    request.form  # type:MultiDict
    request.args  # type:MultiDict
    request.cookies  # type:dict
    request.headers  # type:EnvironHeaders
    request.method  # type:GET/POST
    request.url  # type:str
    request.files
    return 'index'
