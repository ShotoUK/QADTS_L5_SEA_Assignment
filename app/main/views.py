from flask import Flask, request, redirect, abort, render_template
from app.main.forms import NameForm, LoginForm
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from . import main

@main.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@main.route('/user/<name>')
def user(name):
    return '<h1>Hello {}!</h1>'.format(name)

@main.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                formEmail = form.email.data
                formPassword = form.password.data
                dbUser = User.query.filter_by(Email=formEmail).first()
                if dbUser.Email == formEmail and check_password_hash(dbUser.Password,formPassword) == True:
                    return '<h1>This is a valid user!</h1>'
                else:
                    return '<h1>This is not a valid user!<h1>'

        except:
            return '<h1>This is not a registered user! <br> Please contact an administrator<h1>'
    else:
        return render_template('login.html',form=form)
    
@main.route('/user/create', methods=['GET','POST'])
def create_user():
    form = LoginForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                email = form.email.data
                password = form.password.data
                hashed_password = str(generate_password_hash(password, method='scrypt', salt_length=8))
                newUser = User(Email=email, Password=hashed_password)

                db.session.add(newUser)
                db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue saving to database'
    else:
        return render_template('create_user.html',form=form)

