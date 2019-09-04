from flask import g
from functools import wraps

from models import db


def set_db_to_read(func):
    """
    设置使用读数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)
    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)
    return wrapper


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断是否包含了用户信息
        if g.user_id and g.is_refresh == False:  # 如果有, 访问视图
            return f(*args, **kwargs)
        else:
            # 如果没有, 拒绝访问
            return {"message": "Invalid token", 'data': None}, 401

    return wrapper
