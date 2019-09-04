from flask import Blueprint
from flask_restful import Api
from utils.output import output_json
from . import article


# 创建蓝图对象
news_bp = Blueprint('news', __name__)
# 创建Api对象
news_api = Api(news_bp)
# 指定自定义的json返回格式
news_api.representation('application/json')(output_json)


news_api.add_resource(article.ArticleResource, '/v1_0/articles/<int(min=1):article_id>',
                      endpoint='Article')

news_api.add_resource(article.ArticleListResource, '/v1_0/articles',
                      endpoint='ArticleList')