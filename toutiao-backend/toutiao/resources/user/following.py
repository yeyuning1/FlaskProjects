from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import IntegrityError
from flask import g, current_app
import time
from utils.decorators import login_required, set_db_to_write
from models.user import Relation
from models import db
from cache import user_cache as user
from cache import statistic


class FollowingListResource(Resource):
    """
    关注用户
    """
    method_decorators = {
        'post': [login_required, set_db_to_write]
    }

    def post(self):
        """
        关注用户
        """
        # 解析参数
        json_parser = RequestParser()
        json_parser.add_argument('target', required=True, location='json')
        args = json_parser.parse_args()
        target = args.target
        if target == g.user_id:
            return {'message': 'User cannot follow self.'}, 400
        ret = 1

        # 往数据库中存储关注情况
        try:
            follow = Relation(user_id=g.user_id, target_user_id=target, relation=Relation.RELATION.FOLLOW)
            db.session.add(follow)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ret = Relation.query.filter(Relation.user_id == g.user_id,
                                        Relation.target_user_id == target,
                                        Relation.relation != Relation.RELATION.FOLLOW)\
                .update({'relation': Relation.RELATION.FOLLOW})
            db.session.commit()

        if ret > 0:
            timestamp = time.time()
            # 用户的关注列表中缓存层中追加数据
            user.UserFollowingCache(g.user_id).update(target, timestamp)
            # 作者的粉丝列表中缓存层中追加数据
            user.UserFollowersCache(target).update(g.user_id, timestamp)
            # 统计数据的持久化存储
            statistic.UserFollowingCountStorage.incr(g.user_id)
            statistic.UserFansCountStorage.incr(target)

        """发送关注通知"""
        # 获取粉丝的基本信息
        _user = user.UserProfileCache(g.user_id).get()
        _data = {
            'user_id': g.user_id,
            'user_name': _user['name'],
            'user_photo': _user['profile_photo'],
            'timestamp': int(time.time())
        }
        # 将推送通知发送给IM服务器(放入消息队列中)    将消息发送到作者的用户id对应的房间 target="2"
        current_app.siomgr.emit('following notify', _data, room=target)


        return {'target': target}, 201
        