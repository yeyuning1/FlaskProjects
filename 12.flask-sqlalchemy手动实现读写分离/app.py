from flask import Flask

from .decorators import select_write_db, select_read_db
from .user_select import db

app = Flask(__name__)


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/demo'
    SQLALCHEMY_BINDS = {
        "bj_m1": 'mysql://root:mysql@127.0.0.1:3306/demo',
        "bj_m2": 'mysql://root:mysql@127.0.0.1:3306/demo',
        "bj_s1": 'mysql://root:mysql@127.0.0.1:8306/demo',
        "bj_s2": 'mysql://root:mysql@127.0.0.1:8306/demo',
    }
    SQLALCHEMY_CLUSTER = {
        "masters": ["bj_m1", "bj_m2"],
        "slaves": ['bj_s2', 'bj_s2'],
        "default": 'bj_m1'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


app.config.from_object(Config)
db.init_app(app)


# 用户表  一
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)


@app.route('/')
@select_write_db  # 手动选择数据库
def index():
    # 增加数据
    user1 = User(name='zs')
    db.session.add(user1)
    db.session.commit()

    # 查询数据
    users = User.query.all()
    print(users)
    return "index"


if __name__ == '__main__':
    with app.app_context():  # 手动创建应用的上下文
        # 删除所有继承自db.Model的表
        db.drop_all()
        # 创建所有继承自db.Model的表
        db.create_all()
        app.run(debug=True)
