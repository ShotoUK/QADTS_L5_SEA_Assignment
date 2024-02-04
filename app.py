import os
from flask import Flask, request, redirect, abort, render_template
from flask_bootstrap import Bootstrap
from app.main.forms import NameForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_BINDS'] = {'default':'sqlite:///' + os.path.join(basedir,'data.sqlite')}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



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
    
@app.route('/user/create', methods=['GET','POST'])
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

# Models

class Customer(db.Model):
    __tablename__ = 'customer'
    CustomerId = db.Column(db.Integer,primary_key=True)
    ProductId = db.Column(db.Integer,db.ForeignKey('product.ProductId'))
    Name = db.Column(db.String(64))
    Description = db.Column(db.String(64))
    Status = db.Column(db.String(64))
    ContactName = db.Column(db.String(64))
    ContactEmail = db.Column(db.String(64))
    ContactPhone = db.Column(db.String(64))
    AgentId = db.Column(db.Integer,db.ForeignKey('user.UserId'))
    DateCreated = db.Column(db.DateTime , default=datetime.utcnow)
    notes = db.relationship('Note',backref='customer',lazy='dynamic')

    def __repr__(self):
        return '<Customer {}>'.format(self.name)
    
class User(db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(64))
    LastName = db.Column(db.String(64))
    Email = db.Column(db.String(64))
    Password = db.Column(db.String(64))
    Role = db.Column(db.String(64))
    DateCreated = db.Column(db.DateTime , default=datetime.utcnow)

    agent = db.relationship('Customer',backref='user',lazy='dynamic')
    note = db.relationship('Note',backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
class Product(db.Model):
    __tablename__ = 'product'
    ProductId = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(64))
    Description = db.Column(db.String(64))
    Price = db.Column(db.Float)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    customers = db.relationship('Customer',backref='product',lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.name)
    
class Note(db.Model):
    __tablename__ = 'note'
    NoteId = db.Column(db.Integer,primary_key=True)
    CustomerId = db.Column(db.Integer,db.ForeignKey('customer.CustomerId'))
    AgentId = db.Column(db.Integer,db.ForeignKey('user.UserId'))
    Note = db.Column(db.String(64))
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note {}>'.format(self.name)

