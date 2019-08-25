from flask import Flask, current_app, g

# request context: request session
# application context: current_app, g


app1 = Flask(__name__)
app2 = Flask(__name__)

# 以redis客户端对象为例
# 用字符串表示创建的redis客户端
# 为了方便在各个视图中使用，将创建的redis客户端对象保存到flask app中，
# 后续可以在视图中使用current_app.redis_cli获取
app1.redis_cli = 'app1 redis client'
app2.redis_cli = 'app2 redis client'


@app1.route('/route11')
def route11():
    return current_app.redis_cli


@app1.route('/route12')
def route12():
    return current_app.redis_cli


@app2.route('/route21')
def route21():
    return current_app.redis_cli


@app2.route('/route22')
def route22():
    return current_app.redis_cli


def db_query():
    user_id = g.user_id
    user_name = g.user_name
    print('user_id={} user_name={}'.format(user_id, user_name))


@app.route('/')
def get_user_profile():
    g.user_id = 123
    g.user_name = 'itcast'
    db_query()
    return 'hello world'
