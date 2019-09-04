from flask import current_app
from flask_restful import Resource, inputs
from flask_restful.inputs import regex, positive
from flask_restful.reqparse import RequestParser


class SearchResource(Resource):
    def get(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('q', type=regex(r'^.{1,50}$'), location='args', required=True)
        parser.add_argument('page', type=positive, default=1, location='args')
        parser.add_argument('per_page', type=positive, default=10, location='args')
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page
        # 全文检索  匹配标题和内容, 文章状态为已审核
        body = {
            '_source': False,
            'from': (page - 1) * per_page,  # 1 -> 0   2 -> 10  3 -> 20   (page-1) * per_age
            'size': per_page,
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            '_all': args.q
                        }
                    },
                    'filter': {
                        'term': {
                            'status': 2
                        }
                    }
                }
            }
        }
        data = current_app.es.search(index='articles', doc_type='article', body=body)
        resp = dict()
        # 总条数
        resp['total_count'] = data['hits']['total']
        result = []
        # 具体数据
        for article in data['hits']['hits']:
            article_id = article['_id']
            from cache.article import ArticleInfoCache
            article_cache = ArticleInfoCache(article_id)
            article_dict = article_cache.get()
            result.append(article_dict)

        resp['result'] = result
        resp['per_page'] = per_page
        resp['page'] = page
        return resp


class SuggestionResource(Resource):
    """
    联想建议
    """
    def get(self):
        """
        获取联想建议
        """
        # 解析参数
        qs_parser = RequestParser()
        qs_parser.add_argument('q', type=inputs.regex(r'^.{1,500}$'), required=True, location='args')
        args = qs_parser.parse_args()
        q = args.q

        # 先尝试自动补全建议查询
        query = {
            'from': 0,
            'size': 10,
            '_source': False,
            'suggest': {
                'word-completion': {
                    'prefix': q,
                    'completion': {
                        'field': 'suggest'
                    }
                }
            }
        }
        ret = current_app.es.search(index='completions', body=query)
        options = ret['suggest']['word-completion'][0]['options']

        # 如果没得到查询结果，进行纠错建议查询
        if not options:
            query = {
                'from': 0,
                'size': 10,
                '_source': False,
                'suggest': {
                    'text': q,
                    'word-phrase': {
                        'phrase': {
                            'field': '_all',
                            'size': 1
                        }
                    }
                }
            }
            ret = current_app.es.search(index='articles', doc_type='article', body=query)
            options = ret['suggest']['word-phrase'][0]['options']

        results = []
        for option in options:
            if option['text'] not in results:
                results.append(option['text'])

        return {'options': results}