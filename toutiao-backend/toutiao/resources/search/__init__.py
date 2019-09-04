from flask import Blueprint
from flask_restful import Api
from utils.output import output_json
from . import article_search

# 创建蓝图对象
search_bp = Blueprint('search', __name__)
# 创建Api对象
search_api = Api(search_bp)
# 指定自定义的json返回格式
search_api.representation('application/json')(output_json)


search_api.add_resource(article_search.SearchResource, '/v1_0/search',
                      endpoint='Search')


search_api.add_resource(article_search.SuggestionResource, '/v1_0/suggestion',
                      endpoint='Suggest')