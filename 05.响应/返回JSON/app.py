from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    json_dict = {
        'user': 'yyn'
    }
    return jsonify(json_dict)
