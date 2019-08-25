from flask import Flask

app = Flask(__name__)
app.config.from_envvar()  # 从环境变量中取
app.config.from_object()  # 从对象中取
app.config.from_json()  # 从json文件中取
app.config.from_pyfile()  # 从py文件中取

@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)