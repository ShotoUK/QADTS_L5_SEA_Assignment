from .. import db
from datetime import datetime

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