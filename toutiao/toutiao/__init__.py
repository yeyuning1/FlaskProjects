import sys
import os

# 获取到项目的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目中的common目录加入查询路径中 (方便导入common中的模块)
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))

from flask import Flask
from .settings.default import config_dict


def create_flask_app(env_type, enable_config_file=False):
    """
    创建Flask应用
    """
    app = Flask(__name__)
    # 读取环境对应的配置
    config_class = config_dict[env_type]

    # 加载配置
    app.config.from_object(config_class)
    if enable_config_file:
        from utils import constants
        # 加载隐私配置
        app.config.from_envvar(constants.GLOBAL_SETTING_ENV_NAME, silent=True)

    return app


def create_app(env_type, enable_config_file=False):
    """
    创建flask应用 并 初始化各组件

    :param env_type: 环境类型
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: flask应用
    """
    app = create_flask_app(env_type, enable_config_file)

    # 添加自定义正则转换器
    from utils.converters import register_converters
    register_converters(app)

    # TODO 创建redis哨兵
    from redis.sentinel import Sentinel
    _sentinel = Sentinel(app.config['REDIS_SENTINELS'])
    # 获取redis主从连接对象
    app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
    app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])

    # 配置myql数据库
    from models import db
    db.init_app(app)

    # 配置日志
    from utils.logging import create_logger
    create_logger(app)

    # 限流器
    from utils.limiter import limiter as lmt
    lmt.init_app(app)

    # 创建Snowflake ID worker
    from utils.snowflake.id_worker import IdWorker
    app.id_worker = IdWorker(app.config['DATACENTER_ID'],
                             app.config['WORKER_ID'],
                             app.config['SEQUENCE'])

    # 注册用户模块蓝图
    from .resources.user import user_bp
    app.register_blueprint(user_bp)

    # 注册新闻模块蓝图
    from .resources.news import news_bp
    app.register_blueprint(news_bp)

    # 注册搜索模块蓝图
    from .resources.search import search_bp
    app.register_blueprint(search_bp)

    return app

