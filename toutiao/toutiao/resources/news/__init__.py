from flask import Blueprint
from flask_restful import Api
from utils.output import output_json


# 创建蓝图对象
news_bp = Blueprint('news', __name__)
# 创建Api对象
news_api = Api(news_bp)
# 指定自定义的json返回格式
news_api.representation('application/json')(output_json)


