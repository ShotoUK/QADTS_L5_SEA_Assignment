from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm
from ..models import User
from . import auth
from .. import db
import logging


@auth.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()

    try:
        if form.validate_on_submit():

            # logging.info('Attempting to login user.')

            formEmail = form.email.data
            formPassword = form.password.data
            dbUser = User.query.filter_by(Email=formEmail).first()

            if dbUser is not None and dbUser.verify_password(formPassword):
                login_user(user=dbUser)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid username or password.')

            # logging.info('User Logged In.')

        return render_template('login.html',form=form)

    except:

        logging.error('User not logged in.')
        return '<h1>This is not a registered user! <br> Please contact an administrator<h1>'
    
@auth.route('/logout/')
@login_required
def logout():

    try:

        logging.info('Attempting to logout user.')

        logout_user()
        flash('You have been logged out.')

        logging.info('User Logged Out.')

        return redirect(url_for('main.index'))
    
    except:
            
        logging.error('User log out failed.')
        return '<h1>There was an issue logging out the user<h1>'

@auth.route('/register/', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():

                logging.info('Attempting to register user.')

                newUser = User()
                
                # Generate password hash
                newUser.password = form.password.data

                # Set email and password
                newUser.Email = form.email.data
                newUser.Role = 1
                newUser.Confirmed = True

                # Add to database
                db.session.add(newUser)
                db.session.commit()

                flash('You can now login.')

                logging.info('User Registered.')

            return redirect(url_for('main.index'))
        
        except:
            print(form.errors)

            logging.error('User not registered.')
            return '<h1>There was an issue when creating the user<h1>'
    else:

        logging.info('User not registered.')
        return render_template('register.html',form=form)
        
