from flask import render_template, request, redirect, url_for, flash
from main.forms import LoginForm
from models import User
from . import auth


@auth.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                formEmail = form.email.data
                formPassword = form.password.data
                dbUser = User.query.filter_by(Email=formEmail).first()
                if dbUser.verify_password == True:
                    return '<h1>This is a valid user!</h1>'
                else:
                    return '<h1>This is not a valid user!<h1>'

        except:
            return '<h1>This is not a registered user! <br> Please contact an administrator<h1>'
    else:
        return render_template('login.html',form=form)