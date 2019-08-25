from werkzeug.routing import *

DEFAULT_CONVERTERS = {
    'default': UnicodeConverter,
    'string': UnicodeConverter,
    'any': AnyConverter,
    'path': PathConverter,
    'int': IntegerConverter,
    'float': FloatConverter,
    'uuid': UUIDConverter,
}


# 自定义转换器
# 所有转换器继承自
# type: BaseConverter
class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}'
# 创建转换器后 需要在应用中定义