from flask import current_app
from redis import StrictRedis
from sqlalchemy import func
from sqlalchemy.exc import DatabaseError

from cache.statistic import UserArticleCountStorage, UserFollowingCountStorage, UserFollowersCountStorage
from models import db
from models.news import Article


def fix_statistic(flask_app):
    """修改统计数据"""
    # 如果db使用init_app来初始化, 则必须在视图函数中使用, 否则需要手动创建应用上下文
    with flask_app.app_context():
        # 校正作品数量
        __fix_statistic(UserArticleCountStorage)
        # 校正关注数据
        __fix_statistic(UserFollowingCountStorage)
        # 校正粉丝数据
        __fix_statistic(UserFollowersCountStorage)



def __fix_statistic(cls):
    try:
        # 查询出mysql中的数据
        data = cls.db_query()
    except DatabaseError as e:
        current_app.logger.error(e)
    else:
        # 重置redis数据
        cls.reset(data)