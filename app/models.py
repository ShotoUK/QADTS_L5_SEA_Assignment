from . import db
from . import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

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
    
    @staticmethod
    def insert_customers():
        customers = {
            'Global Systems': [1,'Global company that wants Debtsolv','New Lead','John Doe','john@gsystems.com','01614821953'],
            'Tech Solutions': [2,'Wants to resell wallkat','New Lead','Lily Chang','lily@techsolutions.com','02081234567'],
            'Future Industries': [3,'Description 3','Active','Max Davidson','max@futureindustries.com','01619876543'],
            'Meta Enterprises': [4,'Description 4','Inactive','Rachel Bennett','rachel@menterprises.com','01143698520']
        }

        for c in customers:
            customer = Customer.query.filter_by(Name=c).first()
            if customer is None:
                customer = Customer(ProductId=customers[c][0],Name=c,Description=customers[c][1],Status=customers[c][2],ContactName=customers[c][3],ContactEmail=customers[c][4],ContactPhone=customers[c][5])
            db.session.add(customer)
        db.session.commit()
    
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer,primary_key=True)
    FirstName = db.Column(db.String(64))
    LastName = db.Column(db.String(64))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Role = db.Column(db.Integer, default=1)
    DateCreated = db.Column(db.DateTime , default=datetime.utcnow)

    agent = db.relationship('Customer',backref='user',lazy='dynamic')
    note = db.relationship('Note',backref='user',lazy='dynamic')

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.Role is None:
            self.Role = Role.query.filter_by(Default=True).first()

    def is_authenticated(self):
        return True
    
    def get_id(self):
        return str(self.UserId)

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
    
    def can(self,permissions):
        return self.Role is not None and (self.Role & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    
    def is_administrator(self):
        return False
    
class Role(db.Model):
    __tablename__ = 'role'
    RoleId = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(64))
    Default = db.Column(db.Boolean,default=False,index=True)
    Permissions = db.Column(db.Integer)
    # Users = db.relationship('User',backref='Role',lazy='dynamic')

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.Permissions is None:
            self.Permissions = 0

    def __repr__(self):
        return '<Role {}>'.format(self.name)
    
    def add_permission(self,permission):
        if not self.has_permission(permission):
            self.Permissions += permission

    def remove_permission(self,permission):
        if self.has_permission(permission):
            self.Permissions -= permission

    def reset_permissions(self):
        self.Permissions = 0
    
    def has_permission(self,permission):
        return self.Permissions & permission == permission
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.VIEW,Permission.EDIT],
            'Admin': [Permission.VIEW,Permission.EDIT,Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(Name=r).first()
            if role is None:
                role = Role(Name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.Default = (role.Name == default_role)
            db.session.add(role)
        db.session.commit()
    
class Permission:
    VIEW = 1
    EDIT = 2
    ADMIN = 4
    
class Product(db.Model):
    __tablename__ = 'product'
    ProductId = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(128))
    Description = db.Column(db.String(2000))
    Price = db.Column(db.Float)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

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