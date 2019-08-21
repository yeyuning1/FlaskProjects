from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@192.168.42.80/test'
# 设置是否追踪数据库变化   一般不会开启, 影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置是否打印底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
