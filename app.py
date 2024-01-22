from flask import Flask, request, redirect, abort, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}!</h1>'.format(name)