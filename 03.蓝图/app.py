from flask import Flask

app = Flask(__name__)
from .home import home_blu  # 更改导包顺序可能会导致循环导包问题

app.register_blueprint(home_blu)
