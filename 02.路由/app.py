from flask import Flask

app = Flask(__name__)



app.url_map  # 保存 Flask 的路由映射信息
for rule in app.url_map.iter_rules():  # 包含每个路由对象的信息
    rule.endpoint
    rule.rule


@app.route('/', methods=['GET', 'POST'])  # methods 参数为接口定义请求方式
def index():
    pass

