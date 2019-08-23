from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/test'
# 设置是否追踪数据库变化   一般不会开启, 影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置是否打印底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 't_user'  # 设置表名，默认为类名小写
    id = db.Column(db.Integer, primary_key=True)  # 设置为主键
    name = db.Column(db.String(20), unique=True)  # 设置为唯一
    age = db.Column(db.Integer)
    email = db.Column(db.String(30))

    def __repr__(self):
        return '(%s, %s, %s)' % (self.id, self.name, self.age)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # 删除所有表
    db.drop_all()
    # 创建所有表
    db.create_all()
    # 添加测试数据
    user1 = User(name='wang', email='wang@163.com', age=20)
    user2 = User(name='zhang', email='zhang@189.com', age=33)
    user3 = User(name='chen', email='chen@126.com', age=23)
    user4 = User(name='zhou', email='zhou@163.com', age=29)
    user5 = User(name='tang', email='tang@itheima.com', age=25)
    user6 = User(name='wu', email='wu@gmail.com', age=25)
    user7 = User(name='qian', email='qian@gmail.com', age=23)
    user8 = User(name='liu', email='liu@itheima.com', age=30)
    user9 = User(name='li', email='li@163.com', age=28)
    user10 = User(name='sun', email='sun@163.com', age=26)

    # 一次添加多条数据
    db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
    db.session.commit()
    app.run(debug=True)
