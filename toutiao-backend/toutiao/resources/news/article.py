from flask import current_app, g
from flask_restful import Resource, inputs
from flask_restful.inputs import positive
from flask_restful.reqparse import RequestParser

from cache.article import ArticleInfoCache
from utils.logging import write_trace_log
from utils.parser import channel_id


class ArticleResource(Resource):
    """
    文章
    """
    def get(self, article_id):
        """
        获取文章详情
        :param article_id: int 文章id
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('Trace', type=inputs.regex(r'^.+$'), required=False, location='headers')
        args = qs_parser.parse_args()

        # 从缓存层中查询文章数据
        article_cache = ArticleInfoCache(article_id)
        if article_cache.exists():
            article_dict = article_cache.get()

            # 向埋点日志中写入推荐系统需要的埋点信息
            if args.Trace:
                write_trace_log(args.Trace)

            # TODO 从缓存层中查询 文章内容/关注/评论/点赞情况

            # TODO 通过RPC向推荐系统索取相关文章推荐

            return article_dict

        else:
            return {'messsage': 'Invalid article'}, 400


class ArticleListResource(Resource):
    def _get_article_recommands(self, channel_id, article_num, time_stamp):
        """通过grpc获取推荐数据"""
        from rpc.reco_pb2_grpc import RecoStub
        # 创建客户端助手
        stub = RecoStub(current_app.channel)
        # 封装请求参数对象
        from rpc.reco_pb2 import RecoRequestArgs
        args = RecoRequestArgs()
        args.user_id = str(g.user_id) if g.user_id else "annomy"
        args.channel_id = channel_id
        args.article_num = article_num
        args.time_stamp = time_stamp
        # 调用远程函数
        return stub.article_recommand(args)

    def get(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('channel_id', type=channel_id, required=True, location='args')
        parser.add_argument('article_num', type=positive, default=10, location='args')
        parser.add_argument('time_stamp', type=positive, required=True, location='args')
        args = parser.parse_args()

        # 通过grpc向推荐系统索要数据
        data = self._get_article_recommands(args.channel_id, args.article_num, args.time_stamp)
        articles = []
        for article in data.articles:
            article_dict = dict()
            article_id = article.article_id
            article_dict['article_id'] = article_id

            # 根据文章id去缓存层获取数据
            from cache.article import ArticleInfoCache
            article_cache = ArticleInfoCache(article_id)
            acticle_basic_dict = article_cache.get()
            article_dict.update(acticle_basic_dict)

            article_dict['track'] = dict()
            article_dict['track']['click'] = article.track.click
            article_dict['track']['read'] = article.track.read
            article_dict['track']['collect'] = article.track.collect
            articles.append(article_dict)

        return {'pre_time_stamp': data.pre_time_stamp, 'articles': articles}