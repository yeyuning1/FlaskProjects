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

    # redis 集群
    REDIS_CLUSTER = [
        {'host': '127.0.0.1', 'port': '7000'},
        {'host': '127.0.0.1', 'port': '7001'},
        {'host': '127.0.0.1', 'port': '7002'},
    ]

    # 日志
    LOGGING_LEVEL = 'DEBUG'  # 日志级别
    LOGGING_FILE_DIR = '/home/python/logs'  # 日志文件目录
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024  # 日志文件大小
    LOGGING_FILE_BACKUP = 10  # 日志文件数量
    PROPAGATE_EXCEPTIONS = True  # 设置为False, 则flask内置日志会写入文件, 但错误信息将不会显示到网页上

    # sqlalchemy
    SQLALCHEMY_BINDS = {
        "bj_m1": 'mysql://root:mysql@192.168.105.134:3306/toutiao',
        "bj_m2": 'mysql://root:mysql@192.168.105.134:3306/toutiao',
        "bj_s1": 'mysql://root:mysql@192.168.105.134:8306/toutiao',
        "bj_s2": 'mysql://root:mysql@192.168.105.134:8306/toutiao',
    }
    SQLALCHEMY_CLUSTER = {
        "masters": ["bj_m1", "bj_m2"],
        "slaves": ['bj_s2', 'bj_s2'],
        "default": 'bj_m1'
    }  # 数据库连接
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
    SQLALCHEMY_ECHO = False  # 打印底层sql语句

    # Snowflake ID Worker 参数
    DATACENTER_ID = 0
    WORKER_ID = 0
    SEQUENCE = 0

    # JWT
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
    JWT_EXPIRY_HOURS = 2
    JWT_REFRESH_DAYS = 60

    # 七牛云
    QINIU_ACCESS_KEY = 'kJ8wVO7lmFGsdvtI5M7eQDEJ1eT3Vrygb4SmR00E'
    QINIU_SECRET_KEY = 'rGwHyAvnlLK7rU4htRpNYzpuz0OHJKzX2O1LWTNl'
    QINIU_BUCKET_NAME = 'info28'
    QINIU_DOMAIN = 'http://pwu6b2esm.bkt.clouddn.com/'

 	# rpc
    class RPC:
        RECOMMEND = '192.168.42.70:8900'
        CHATBOT = '172.17.0.59:9999'

    RABBIT_MQ = 'amqp://guest:guest@192.168.105.128:5672'  # 消息队列的地址

    # es
    ES_HOST = ['127.0.0.1:9200']


class TestingConfig(DefaultConfig):
    TESTING = True  # 开启测试模式, flask就不再内部进行异常捕获, 方便查询到具体的报错位置


config_dict = {
    'dev': DefaultConfig,
    'test': TestingConfig
}