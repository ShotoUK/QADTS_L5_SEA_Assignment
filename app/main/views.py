from flask import Flask, request, redirect, abort, render_template
from flask_login import login_required
from app.main.forms import NameForm, LoginForm, CreateUserForm
from .. import db
from app.models import User, Customer
from . import main

@main.route('/', methods=['GET','POST'])
@login_required
def index():
    name = None
    customers = Customer.query.all()
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name, customers=customers)

@main.route('/customer/<int:id>', methods=['GET','POST'])
@login_required
def customerdetail(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer.html', customer=customer)
  
@main.route('/user/create', methods=['GET','POST'])
@login_required
def create_user():
    form = CreateUserForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                newUser = User()
                
                # Generate password hash
                newUser.password = form.password.data

                # Set email and password
                newUser.Email = form.email.data
                newUser.Password = newUser.password_hash

                # Add to database
                db.session.add(newUser)
                db.session.commit()
            return render_template('usercreated.html')
        except:
            return 'There was an issue saving to database'
    else:
        return render_template('createuser.html',form=form)

