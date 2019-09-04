import json
from sqlalchemy.orm import load_only
from flask import current_app
from redis.exceptions import RedisError

from models.news import Channel
from . import constants


class AllChannelsCache(object):
    """
    全部频道缓存
    """
    key = 'ch:all'

    @classmethod
    def get(cls):
        """
        获取
        :return: [{'name': 'python', 'id': '123'}, {}]
        """
        rc = current_app.redis_cluster

        # 缓存取数据
        ret = rc.get(cls.key)
        if ret:
            results = json.loads(ret)
            return results

        # 数据库查询
        results = []

        channels = Channel.query.options(load_only(Channel.id, Channel.name)) \
            .filter(Channel.is_visible == True).order_by(Channel.sequence, Channel.id).all()

        if not channels:
            return results

        for channel in channels:
            results.append({
                'id': channel.id,
                'name': channel.name
            })

        # 设置缓存
        try:
            rc.setex(cls.key, constants.ALL_CHANNELS_CACHE_TTL, json.dumps(results))
        except RedisError as e:
            current_app.logger.error(e)

        return results

    @classmethod
    def exists(cls, channel_id):
        """
        判断channel_id是否存在
        :param channel_id: 频道id
        :return: bool
        """
        # 此处不直接用redis判断是否存在键值
        # 先从redis中判断是否存在键，再从键判断值是否存在，redis集群中无法保证事务
        chs = cls.get()
        for ch in chs:
            if channel_id == ch['id']:
                return True
        return False