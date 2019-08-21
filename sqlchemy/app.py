from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@192.168.42.80/test'
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


@app.route('/')
def hello_world():
    db.drop_all()
    db.create_all()


    return 'Hello World!'


if __name__ == '__main__':


    app.run(debug=True)
