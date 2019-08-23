from flask import Blueprint
from flask_restful import Api

from utils.output import output_json

# 创建蓝图对象
user_bp = Blueprint('user', __name__)
# 创建Api对象
user_api = Api(user_bp)
# 指定自定义的json返回格式
user_api.representation('application/json')(output_json)

