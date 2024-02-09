from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from .forms import LoginForm
from ..models import User
from . import auth


@auth.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()

    try:
        if form.validate_on_submit():
            formEmail = form.email.data
            formPassword = form.password.data
            dbUser = User.query.filter_by(Email=formEmail).first()
            if dbUser is not None and dbUser.verify_password(formPassword):
                # TODO: Fix this
                login_user(dbUser)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid username or password.')
        return render_template('login.html',form=form)

    except:
        return '<h1>This is not a registered user! <br> Please contact an administrator<h1>'
