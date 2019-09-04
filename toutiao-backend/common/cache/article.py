from sqlalchemy.orm import load_only
from flask_restful import fields, marshal
import json
from flask import current_app
from redis.exceptions import RedisError

from cache.user_cache import UserProfileCache
from models.news import Article
from . import constants
from cache import statistic as cache_statistic


class ArticleInfoCache(object):
    """
    文章基本信息缓存
    """
    article_info_fields_db = {
        'title': fields.String(attribute='title'),
        'aut_id': fields.Integer(attribute='user_id'),
        'pubdate': fields.DateTime(attribute='ctime', dt_format='iso8601'),
        'ch_id': fields.Integer(attribute='channel_id')
    }

    def __init__(self, article_id):
        self.key = 'art:{}:info'.format(article_id)
        self.article_id = article_id

    def save(self):
        """
        保存文章缓存
        """
        rc = current_app.redis_cluster

        article = Article.query.options(load_only(Article.id, Article.title, Article.user_id, Article.channel_id,
                                                  Article.cover, Article.ctime))\
            .filter_by(id=self.article_id, status=Article.STATUS.APPROVED).first()
        if article is None:
            return

        article_formatted = marshal(article, self.article_info_fields_db)
        article_formatted['cover'] = article.cover

        try:
            rc.setex(self.key, constants.ArticleInfoCacheTTL.get_val(), json.dumps(article_formatted))
        except RedisError as e:
            current_app.logger.error(e)

        return article_formatted

    def _fill_fields(self, article_formatted):
        """
        补充字段
        """
        article_formatted['art_id'] = self.article_id
        # 获取作者名
        author = UserProfileCache(article_formatted['aut_id']).get()
        article_formatted['aut_name'] = author['name']
        article_formatted['comm_count'] = cache_statistic.ArticleCommentCountStorage.get(self.article_id)
        return article_formatted

    def get(self):
        """
        获取文章
        :return: {}
        """
        rc = current_app.redis_cluster

        # 从缓存中查询
        try:
            article = rc.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            article = None

        if article:
            article_formatted = json.loads(article)
        else:
            article_formatted = self.save()

        if not article_formatted:
            return None

        article_formatted = self._fill_fields(article_formatted)

        return article_formatted

    def exists(self):
        """
        判断文章是否存在
        :return: bool
        """
        rc = current_app.redis_cluster

        # 此处可使用的键有三种选择 user:{}:profile 或 user:{}:status 或 新建
        # status主要为当前登录用户，而profile不仅仅是登录用户，覆盖范围更大，所以使用profile
        try:
            ret = rc.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret is not None:
            return False if ret == b'-1' else True
        else:
            # 缓存中未查到
            article = self.save()
            if article is None:
                return False
            else:
                return True


    def clear(self):
        rc = current_app.redis_cluster
        rc.delete(self.key)




