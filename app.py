from flask import Flask, request, redirect, abort, render_template
from forms import NameForm, LoginForm

app = Flask(__name__)
# TODO: Needs to be saved in a environment variable
app.config['SECRET_KEY'] = 'WkmpPFr+Sw9Nz5:6EM3;Zq'

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500



