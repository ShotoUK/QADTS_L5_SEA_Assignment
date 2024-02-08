from flask import Flask, request, redirect, abort, render_template
from app.main.forms import NameForm, LoginForm, CreateUserForm
from .. import db
from app.models import User
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
    
@main.route('/user/create', methods=['GET','POST'])
def create_user():
    form = CreateUserForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                email = form.email.data
                newUser = User(Email=email)
                newUser.password = form.password.data

                db.session.add(newUser)
                db.session.commit()
            return render_template('usercreated.html')
        except:
            return 'There was an issue saving to database'
    else:
        return render_template('createuser.html',form=form)

