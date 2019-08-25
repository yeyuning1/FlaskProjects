class BaseConfig(object):
    BASE_URL = 'yeyuning,cn'


class DevConfig(BaseConfig):
    pass


class ProConfig(BaseConfig):
    pass


config_map = {
    'default': DevConfig,
    'dev': DevConfig,
    'pro': ProConfig
}
