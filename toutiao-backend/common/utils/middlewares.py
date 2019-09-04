from flask import request, g
from utils.jwt_util import verify_jwt


def jwt_authentication():
    """
    获取和校验jwt
    """
    g.user_id = None
    g.is_refresh = False
    # 获取token
    header = request.headers.get('Authorization')
    if header and header.startswith('Bearer '):
        token = header[7:]
        # 校验token
        payload = verify_jwt(token)
        if payload:
            # 使用g变量来记录用户信息
            g.user_id = payload.get("user_id")
            g.is_refresh = payload.get("is_refresh")
