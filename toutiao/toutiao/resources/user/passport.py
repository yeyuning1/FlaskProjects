from flask_restful import Resource
from flask import current_app, request
import random
from celery_tasks.sms.tasks import send_verification_code
from . import constants
from utils.limiter import limiter as lmt
from flask_limiter.util import get_remote_address


class SMSVerificationCodeResource(Resource):
    """
    获取短信验证码
    """
    error_message = 'Too many requests.'

    decorators = [
        lmt.limit(constants.LIMIT_SMS_VERIFICATION_CODE_BY_MOBILE,
                  key_func=lambda: request.view_args['mobile'],
                  error_message=error_message),
        lmt.limit(constants.LIMIT_SMS_VERIFICATION_CODE_BY_IP,
                  key_func=get_remote_address,
                  error_message=error_message)
    ]

    def get(self, mobile):
        # 生成验证码
        code = '{:0>6d}'.format(random.randint(0, 999999))
        # 保存到redis中
        current_app.redis_master.setex('app:code:{}'.format(mobile), constants.SMS_VERIFICATION_CODE_EXPIRES, code)
        # 使用celery异步任务 发送短信
        send_verification_code.delay(mobile, code)
        return {'mobile': mobile}











