from flask_restful import Resource
from flask import current_app
import random
from celery_tasks.sms.tasks import send_verification_code
from . import constants


class SMSVerificationCodeResource(Resource):
    """
    获取短信验证码
    """
    def get(self, mobile):
        # 生成验证码
        code = '{:0>6d}'.format(random.randint(0, 999999))
        # 保存到redis中
        current_app.redis_master.setex('app:code:{}'.format(mobile), constants.SMS_VERIFICATION_CODE_EXPIRES, code)
        # 使用celery异步任务 发送短信
        send_verification_code.delay(mobile, code)
        return {'mobile': mobile}











