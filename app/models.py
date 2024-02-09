from . import db
from . import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Customer(db.Model):
    __tablename__ = 'customer'
    CustomerId = db.Column(db.Integer,primary_key=True)
    ProductId = db.Column(db.Integer,db.ForeignKey('product.ProductId'))
    Name = db.Column(db.String(128))
    Description = db.Column(db.String(5000))
    Status = db.Column(db.String(64))
    ContactName = db.Column(db.String(128))
    ContactEmail = db.Column(db.String(128))
    ContactPhone = db.Column(db.String(64))
    AgentId = db.Column(db.Integer,db.ForeignKey('user.UserId'))
    DateCreated = db.Column(db.DateTime , default=datetime.utcnow)
    notes = db.relationship('Note',backref='customer',lazy='dynamic')

    def __repr__(self):
        return '<Customer {}>'.format(self.name)
    
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(64))
    LastName = db.Column(db.String(64))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Role = db.Column(db.String(128))
    DateCreated = db.Column(db.DateTime , default=datetime.utcnow)

    agent = db.relationship('Customer',backref='user',lazy='dynamic')
    note = db.relationship('Note',backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.Password = generate_password_hash(password, method='scrypt', salt_length=8)

    def verify_password(self,password):
        return check_password_hash(self.Password,password)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
class Product(db.Model):
    __tablename__ = 'product'
    ProductId = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(128))
    Description = db.Column(db.String(2000))
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
    Note = db.Column(db.String(2000))
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note {}>'.format(self.name)