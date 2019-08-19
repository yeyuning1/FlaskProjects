class BaseConfig(object):
    SQL_URL = 'mysql://192.168.42.80:3306'


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    SQL_URL = 'mysql://127.0.0.1:3306'


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
