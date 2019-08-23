class DefaultConfig(object):
    """
    Flask默认配置
    """
    # redis 哨兵
    REDIS_SENTINELS = [
        ('127.0.0.1', '26380'),  # 哨兵ip+端口
        ('127.0.0.1', '26381'),
        ('127.0.0.1', '26382'),
    ]
    REDIS_SENTINEL_SERVICE_NAME = 'mymaster'  # 主数据库别名


config_dict = {
    'dev': DefaultConfig
}