"""
用户作品数量的统计类
属性
key redis的键
方法
get 获取数据
update  更新数据
"""
from flask import current_app
from redis import StrictRedis, RedisError
from sqlalchemy import func

from models import db
from models.news import Article, Comment
from models.user import Relation


class BaseCountStorage:
    @classmethod
    def get(cls, user_id):
        """
        获取统计数量
        :param user_id: 用户id
        :return: 统计数量
        """
        # 从redis中取出数据
        redis_slave = current_app.redis_slave  # type: StrictRedis
        try:
            count = redis_slave.zscore(cls.key, user_id)  # 如果有值,返回float类型, 没有返回None
        except RedisError as e:
            current_app.logger.error(e)
            raise e
        # 返回数据
        if count:
            return int(count)
        else:
            return 0

    @classmethod
    def update(cls, user_id, count=1):
        """
        更新统计数量
        :param user_id: 用户id
        :param count: 数量变化 如果要减少 count=-1
        """
        # 对redis数据进行更新
        redis_master = current_app.redis_master  # type: StrictRedis
        try:
            redis_master.zincrby(cls.key, user_id, count)
        except RedisError as e:  # 不处理, 结果mysql和redis的数据不一致
            current_app.logger.error(e)

    @classmethod
    def reset(cls, db_data):
        # 删除redis中的数据
        redis_master = current_app.redis_master  # type: StrictRedis

        # 将mysql的数据更新到redis中
        tmp_key = cls.key + ":tmp"
        try:
            for user_id, count in db_data:
                # 将数据先放入临时集合中
                redis_master.zadd(tmp_key, count, user_id)

            # 当数据全部更新完成后, 再重命名键(删除原集合, 新集合使用对应的键)
            redis_master.rename(tmp_key, cls.key)
        except RedisError as e:
            current_app.logger.error(e)
            redis_master.delete(tmp_key)


class UserArticleCountStorage(BaseCountStorage):
    """用户作品数量的统计类 count:user:arts  zset  [{value: 用户id, score:作品数}]"""
    key = 'count:user:arts'

    @classmethod
    def db_query(cls):
        return db.session.query(Article.user_id, func.count(Article.id)).group_by(Article.user_id).filter(
            Article.status == Article.STATUS.APPROVED).all()

class UserFollowingCountStorage(BaseCountStorage):
    """用户关注数量统计类"""
    key = 'count:user:followings'

    @classmethod
    def db_query(cls):
        return db.session.query(Relation.user_id, func.count(Relation.id)).group_by(Relation.user_id).filter(
            Relation.relation == Relation.RELATION.FOLLOW).all()

class UserFollowersCountStorage(BaseCountStorage):
    """用户粉丝数量统计类"""
    key = 'count:user:followers'

    @classmethod
    def db_query(cls):
        return db.session.query(Relation.target_user_id, func.count(Relation.id)).group_by(Relation.target_user_id).filter(
            Relation.relation == Relation.RELATION.FOLLOW).all()


class ArticleCommentCountStorage(BaseCountStorage):
    """
    文章评论数量
    """
    key = 'count:art:comm'

    @staticmethod
    def db_query():
        ret = db.session.query(Comment.article_id, func.count(Comment.id)).filter(Comment.status == Comment.STATUS.APPROVED).group_by(Comment.article_id).all()
        return ret