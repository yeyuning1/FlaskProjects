from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from cache.statistic import UserArticleCountStorage, UserFollowingCountStorage, UserFollowersCountStorage
from cache.user_cache import UserProfileCache
from models import db
from models.user import User
from utils.decorators import login_required
from utils.image_storage import upload_file
from utils.parser import image_file


class PhotoResource(Resource):
    method_decorators = {'patch': [login_required]}
    def patch(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('photo', location='files', required=True ,type=image_file)
        args = parser.parse_args()
        f = args.photo

        # f = request.files  # type: FileStorage
        # f.save()
        # f.read()

        # 读取上传的二进制数据
        img_bytes = f.read()

        # 上传到七牛云
        try:
            file_name = upload_file(img_bytes)
            # 更新数据库中头像的URL
            User.query.filter(User.id == g.user_id).update({'profile_photo': file_name})
            db.session.commit()
            # 删除缓存数据
            user_cache = UserProfileCache(g.user_id)
            user_cache.clear()
            # 返回头像的URL
            return current_app.config['QINIU_DOMAIN'] + file_name

        except BaseException as e:
            current_app.logger.error(e)
            return {"message": "Third System error", "data": None}, 500


class CurrentUserProfileResoure(Resource):
    method_decorators = [login_required]

    def get(self):
        # 使用缓存类来读取数据
        user_cache = UserProfileCache(g.user_id)
        # 添加一条测试数据
        UserArticleCountStorage.update(g.user_id)

        # 校验用户数据
        if user_cache.exist():
            user_dict = user_cache.get()
            user_dict['art_count'] = UserArticleCountStorage.get(g.user_id)
            user_dict['following_count'] = UserFollowingCountStorage.get(g.user_id)
            user_dict['followers_count'] = UserFollowersCountStorage.get(g.user_id)
            # 返回数据
            return user_dict
        else:
            return {'message': "Invalid User", 'data': None}, 400
