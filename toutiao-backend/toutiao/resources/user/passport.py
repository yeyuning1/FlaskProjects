from flask_restful import Resource
from flask import current_app, request, g
import random
from celery_tasks.sms.tasks import send_verification_code
from utils.jwt_util import generate_jwt
from . import constants
from utils.limiter import limiter as lmt
from flask_limiter.util import get_remote_address
from flask_restful.reqparse import RequestParser
from utils.decorators import set_db_to_write, login_required
from utils.parser import mobile as type_mobile
from models import db
from models.user import User, UserProfile
from flask_restful.inputs import regex
from datetime import datetime, timedelta


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


class AuthorizationResoucre(Resource):
    method_decorators = {'post': [set_db_to_write],
                         'get': [login_required]}  # 选择主数据库

    def _generate_tokens(self, user_id, with_refresh_token=True):
        """生成访问token和刷新token

        :param user_id 用户主键
        :return 访问token 和 刷新token
        """
        # 生成访问token
        access_token = generate_jwt({'user_id': user_id, 'is_refresh': False}, expiry=datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS']))
        # 生成刷新token
        if with_refresh_token:
            refresh_token = generate_jwt({'user_id': user_id, 'is_refresh': True},
                                    expiry=datetime.utcnow() + timedelta(days=current_app.config['JWT_REFRESH_DAYS']))
        else:
            refresh_token = None

        return access_token, refresh_token

    def post(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('mobile', type=type_mobile, required=True, location='json')
        parser.add_argument('code', type=regex(r'^\d{6}$'), required=True, location='json')
        args = parser.parse_args()
        mobile = args.mobile
        code = args.code

        # 校验短信验证码
        key = "app:code:{}".format(mobile)
        try:
            real_code = current_app.redis_master.get(key)
        except BaseException as e:
            current_app.logger.error(e)  # 记录日志
            real_code = current_app.redis_slave.get(key)  # 如果主数据库连接失败, 再到数据库中获取

        # 一旦取出, 验证码就要删除 (验证码只能使用一次)
        # try:
        #     current_app.redis_master.delete(key)
        # except BaseException as e:
        #     current_app.logger.error(e)

        if not real_code or real_code.decode() != code:
            return {'message': "Invalid code", "data": None}, 400

        # 到数据库中查询该用户
        user = User.query.filter_by(mobile=mobile).first()

        if not user:  # 如果没有, 生成一条新的用户数据
            # 生成分布式id
            user_id = current_app.id_worker.get_id()
            # 添加user记录
            user = User(id=user_id, mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
            # 添加user_profile记录
            user_profile = UserProfile(id=user_id)
            db.session.add(user_profile)
        else:
            user.last_login = datetime.now()
            user_id = user.id

        db.session.commit()

        # 记录用户状态, 生成jwt
        access_token, refresh_token = self._generate_tokens(user_id)

        # 返回json数据
        return {'access_token': access_token, "refresh_token": refresh_token}

    def get(self):
        """进行访问测试"""
        return {'user_id': g.user_id, 'is_refresh': g.is_refresh}

    def put(self):
        """生成新的访问token"""
        # 先校验刷新token
        if g.user_id and g.is_refresh == True:
            # 生成新的访问token
            access_token, refresh_token = self._generate_tokens(g.user_id, with_refresh_token=False)
            # 返回数据
            return {'access_token': access_token}, 201
        else:
            return {'message': "Invalid token", 'data': None}, 401








