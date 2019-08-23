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

    # 日志
    LOGGING_LEVEL = 'DEBUG'  # 日志级别
    LOGGING_FILE_DIR = '/home/python/logs'  # 日志文件目录
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024  # 日志文件大小
    LOGGING_FILE_BACKUP = 10  # 日志文件数量
    PROPAGATE_EXCEPTIONS = True  # 设置为False, 则flask内置日志会写入文件, 但错误信息将不会显示到网页上

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao'  # 数据库连接
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
    SQLALCHEMY_ECHO = False  # 打印底层sql语句


config_dict = {
    'dev': DefaultConfig
}