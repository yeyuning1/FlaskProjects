from flask import jsonify
from toutiao import create_app  # 主动执行文件不能使用from . import xx的语法

# 创建flask应用
app = create_app('dev', enable_config_file=True)


@app.route('/')
def route_map():
    """
    主视图，返回所有视图网址
    """
    rules_iterator = app.url_map.iter_rules()
    return jsonify({rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')})
