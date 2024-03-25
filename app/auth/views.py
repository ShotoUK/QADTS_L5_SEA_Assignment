from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from ..models import User
from . import auth
from .. import db
import logging
from ..email import send_email


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

                # Send confirmation email
                token = newUser.generate_confirmation_token()
                send_email(newUser.Email,'Confirm Your Account','auth/email/confirm',user=newUser,token=token)

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
    
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.Confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        current_user.Confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.Email,'Confirm Your Account','auth/email/confirm',user=current_user,token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        
        if not current_user.Confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
        
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.Confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.Email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/resetpasswordrequest.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/resetpassword.html', form=form, token=token)

        
