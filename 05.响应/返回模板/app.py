from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    str1 = 'hello'
    return render_template('index.html', my_str=str1)
