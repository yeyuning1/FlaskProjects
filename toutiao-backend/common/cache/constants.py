import random

# 用户搜索历史每人保存数目
SEARCHING_HISTORY_COUNT_PER_USER = 4

# 全部频道缓存有效期，秒
ALL_CHANNELS_CACHE_TTL = 24 * 60 * 60


class BaseCacheTTL:
    TTL = 60 * 10  # 过期时间
    MaxDelta = 60  # 随机值(防止缓存雪崩)

    @classmethod
    def get_val(cls):
        return cls.TTL + random.randint(0, cls.MaxDelta)


class UserProfileCacheTTL(BaseCacheTTL):
    """用户缓存过期时间类"""
    TTL = 60 * 60 * 2  # 过期时间
    MaxDelta = 600  # 随机值(防止缓存雪崩)


class UserNotExistCacheTTL(BaseCacheTTL):
    """用户数据不存在的过期时间类"""
    pass


class UserFollowingCacheTTL(BaseCacheTTL):
    """用户关注列表的过期时间类"""
    TTL = 60 * 30

class UserFansCacheTTL(BaseCacheTTL):
    """
    用户粉丝列表缓存时间，秒
    """
    TTL = 30 * 60


class ArticleInfoCacheTTL(BaseCacheTTL):
    """
    文章信息缓存时间，秒
    """
    TTL = 30 * 60


class ArticleNotExistsCacheTTL(BaseCacheTTL):
    """
    文章不存在结果缓存
    为解决缓存击穿，有效期不宜过长
    """
    TTL = 5 * 60
    MAX_DELTA = 60