"""
用户缓存类  user:<用户id>:profile   string   "{mobile:xx, nickname:xx}"
属性
user_id
key
方法
get 获取缓存数据
clear 清空缓存数据
"""
import json
import time

from flask import current_app
from redis import RedisError
from rediscluster import StrictRedisCluster
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import load_only

from cache import constants
from cache.constants import UserProfileCacheTTL, UserNotExistCacheTTL
from cache.statistic import UserFollowersCountStorage
from models import db
from models.user import User, Relation


class UserProfileCache:
    """用户数据缓存类"""

    def __init__(self, user_id):
        self.user_id = user_id  # 用户id
        self.key = "user:{}.profile".format(self.user_id)  # redis键

    def save(self):
        """查询数据库, 并写入缓存"""
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            user = User.query.options(
                load_only(User.mobile, User.name, User.profile_photo, User.certificate, User.introduction)).filter(
                User.id == self.user_id).first()
        except DatabaseError as e:
            current_app.logger.error(e)
            raise e  # 主动抛出异常, 让视图层来处理下一步的逻辑

        user_dict = {
            'id': self.user_id,
            'name': user.name,
            'mobile': user.mobile,
            'profile_photo': user.profile_photo,
            'certificate': user.certificate,
            'introduction': user.introduction
        }
        if user:  # 数据库如果有, 将数据回填到缓存中, 再返回数据
            try:
                cluster.set(self.key, json.dumps(user_dict), ex=UserProfileCacheTTL.get_val())
            except RedisError as e:
                current_app.logger.error(e)

            return user_dict

        else:  # 数据库如果没有, 在缓存中设置默认值 -1, 返回None
            try:
                cluster.set(self.key, '-1', ex=UserNotExistCacheTTL.get_val())
            except RedisError as e:
                current_app.logger.error(e)
            return None

    def get(self):
        # 先从缓存中读取数据
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            data = cluster.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            data = None

        # 如果有, 判断是否为默认值
        if data:
            if data == b'-1':  # 如果是默认值, 返回None
                return None
            else:  # 如果不是默认值, 返回数据
                return json.loads(data)

        else:  # 如果没有, 从数据库中读取数据
            return self.save()


    def clear(self):
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            cluster.delete(self.key)  # 删除缓存对应的键
        except RedisError as e:
            current_app.logger.error(e)
            raise e

    def exist(self):
        """校验用户数据是否存在
        :return True/False
        """
        # 先从缓存中读取数据
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            data = cluster.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            data = None

        # 如果有, 判断是否为默认值
        if data:
            if data == b'-1':  # 如果是默认值, 返回False
                return False
            else:  # 如果不是默认值, 返回数据
                return True

        else:  # 如果没有, 从数据库中读取数据
           user_data = self.save()
           return True if user_data else False


class UserFollowingCache:  # user:<用户id>:followings  zset  [{value: 用户id, score: 关注时间}, {}, {}]
    """用户关注列表缓存类"""

    def __init__(self, user_id):
        self.user_id = user_id  # 用户id
        self.key = "user:{}:following".format(user_id)  # redis的键

    def save(self):
        """查询数据库, 并将数据保存到缓存中"""
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            # 查询该用户的关注列表
            # select 用户id, 关注时间 from t_relation where t_relation.user_id=<用户id> and t_relation.relatiion = 1
            data = db.session.query(Relation.target_user_id, Relation.utime).filter(Relation.user_id==self.user_id, Relation.relation == Relation.RELATION.FOLLOW).all()  # [(1, 2019-09-11), (), ()]
        except DatabaseError as e:
            current_app.logger.error(e)
            raise e  # 如果数据库不能查询, 将错误抛给上层 (让视图来确定后续的逻辑, 如重试, 再调用get / 取消 返回500)

        from .constants import UserProfileCacheTTL, UserNotExistCacheTTL

        if len(data):  # 如果数据库中有, 先将数据回填到缓存中, 然后返回数据

            # 将数据回填到缓存中
            following_list = []
            try:
                for target_user_id, following_time in data:
                    cluster.zadd(self.key, following_time.timestamp(), target_user_id)
                    following_list.append(target_user_id)

                from cache.constants import  UserFollowingCacheTTL
                cluster.expire(self.key, UserFollowingCacheTTL().get_val())  # 设置过期时间

            except RedisError as e:
                current_app.logger.error(e)

            return following_list

        else:   # 数据库没有数据, 返回空列表
            return []

    def get(self):
        """读取用户数据

        :return 用户数据 字典/None
        """
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        # 先从缓存中读取数据
        try:
            following_list = cluster.zrevrange(self.key, 0, -1)  # zrevrange一定返回  [b'3', b'4', b'5']
        except RedisError as e:
            current_app.logger.error(e)  # 记录日志
            following_list = []  # 如果redis查询失败, 还可以选择去数据库中查询

        if len(following_list):  # 如果缓存中有, 直接返回关注列表

            return [int(target_user_id) for target_user_id in following_list]  # [3, 4, 5]

        else:  # 如果缓存中没有, 再从数据库中进行查询
            # 根据关注数量来判断该用户关注过别人(数据库是否有数据)
            from cache.statistic import UserFollowingCountStorage
            if UserFollowingCountStorage.get(self.user_id) > 0:  # 有关注数量, 说明数据库有数据
                self.save()
            else:
                return []

    def update(self, timestamp, target_user_id, increament=1):
        """往关注列表中添加一个用户"""
        cluster = current_app.redis_cluster  # type: StrictRedisCluster
        try:
            if increament > 0:  # 关注用户
                cluster.zadd(self.key, timestamp, target_user_id)
            else:  # 取消关注
                cluster.zrem(self.key, target_user_id)

        except RedisError as e:
            current_app.logger.error(e)
            raise e

    def determine_following_target(self, target_id):
        """判断是否关注了指定的用户
        :return True/False 是否关注了该用户
        """
        following_list = self.get()
        return target_id in following_list


class UserFollowersCache(object):
    """
    用户粉丝缓存
    """
    def __init__(self, user_id):
        self.key = 'user:{}:fans'.format(user_id)
        self.user_id = user_id

    def get(self):
        """
        获取用户的粉丝列表
        :return:
        """
        rc = current_app.redis_cluster

        try:
            ret = rc.zrevrange(self.key, 0, -1)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret:
            # In order to be consistent with db data type.
            return [int(uid) for uid in ret]

        ret = UserFollowersCountStorage.get(self.user_id)
        if ret == 0:
            return []

        ret = Relation.query.options(load_only(Relation.user_id, Relation.utime))\
            .filter_by(target_user_id=self.user_id, relation=Relation.RELATION.FOLLOW)\
            .order_by(Relation.utime.desc()).all()

        followers = []
        cache = []
        for relation in ret:
            followers.append(relation.user_id)
            cache.append(relation.utime.timestamp())
            cache.append(relation.user_id)

        if cache:
            try:
                pl = rc.pipeline()
                pl.zadd(self.key, *cache)
                pl.expire(self.key, constants.UserFansCacheTTL().get_val())
                results = pl.execute()
                if results[0] and not results[1]:
                    rc.delete(self.key)
            except RedisError as e:
                current_app.logger.error(e)

        return followers

    def update(self, target_user_id, timestamp, increment=1):
        """
        更新粉丝数缓存
        """
        rc = current_app.redis_cluster
        try:
            if increment > 0:
                rc.zadd(self.key, timestamp, target_user_id)
            else:
                rc.zrem(self.key, target_user_id)
        except RedisError as e:
            current_app.logger.error(e)


class UserSearchingHistoryStorage(object):
    """
    用户搜索历史
    """
    def __init__(self, user_id):
        self.key = 'user:{}:his:searching'.format(user_id)
        self.user_id = user_id

    def save(self, keyword):
        """
        保存用户搜索历史
        :param keyword: 关键词
        :return:
        """
        pl = current_app.redis_master.pipeline()
        pl.zadd(self.key, time.time(), keyword)
        pl.zremrangebyrank(self.key, 0, -1*(constants.SEARCHING_HISTORY_COUNT_PER_USER+1))
        pl.execute()

    def get(self):
        """
        获取搜索历史
        """
        try:
            keywords = current_app.redis_master.zrevrange(self.key, 0, -1)
        except ConnectionError as e:
            current_app.logger.error(e)
            keywords = current_app.redis_slave.zrevrange(self.key, 0, -1)

        keywords = [keyword.decode() for keyword in keywords]
        return keywords

    def clear(self):
        """
        清除
        """
        current_app.redis_master.delete(self.key)