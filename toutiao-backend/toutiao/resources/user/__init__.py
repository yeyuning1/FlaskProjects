from flask import Blueprint
from flask_restful import Api

from utils.output import output_json
from . import passport, userinfo, following

# 创建蓝图对象
user_bp = Blueprint('user', __name__)
# 创建Api对象
user_api = Api(user_bp)
# 指定自定义的json返回格式
user_api.representation('application/json')(output_json)

# 添加类视图
user_api.add_resource(passport.SMSVerificationCodeResource, '/v1_0/sms/codes/<mobile:mobile>',
                      endpoint='SMSVerificationCode')

user_api.add_resource(passport.AuthorizationResoucre, '/v1_0/authorizations',
                      endpoint='Authorization')

user_api.add_resource(userinfo.PhotoResource, '/v1_0/user/photo',
                      endpoint='Photo')

user_api.add_resource(userinfo.CurrentUserProfileResoure, '/v1_0/user',
                      endpoint='CurrentUser')

user_api.add_resource(following.FollowingListResource, '/v1_0/following',
                      endpoint='Following')