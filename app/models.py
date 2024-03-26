from . import db
from . import login_manager
from flask import current_app
from jwt import encode, decode
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

class Customer(db.Model):
    __tablename__ = 'customer'
    CustomerId = db.Column(db.Integer,primary_key=True)
    ProductId = db.Column(db.Integer)
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
    DateCreated = db.Column(db.DateTime , default=datetime.now)
    Confirmed = db.Column(db.Boolean,default=True)

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
    
    
    def generate_confirmation_token(self, expiration=3600):
        token = encode({"confirm": self.UserId, "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration) },current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    
    def confirm(self,token):
        try:
            data = decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=['HS256']
            )
        except:
            return False
        if data.get('confirm') != self.UserId:
            return False
        self.confirmed = True
        db.session.add(self)
        # db.session.commit()
        return True
    
    def generate_reset_token(self,expiration=3600):
        token = encode(
            {
            "reset": self.UserId, 
             "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration) 
             },
             current_app.config['SECRET_KEY'], 
             algorithm='HS256'         
                       )
        return token
    
    @staticmethod
    def reset_password(token,new_password):
        try:
            data = decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=['HS256']
            )
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
    
    @staticmethod
    def insert_adminuser():
        users = {
            'admin': ['Admin','User','charlton.reid@tigersolv.com','password','7']
        }
        for u in users:
            user = User.query.filter_by(Email=u).first()
            if user is None:
                user = User(FirstName=users[u][0],LastName=users[u][1],Email=users[u][2],password=users[u][3])
            db.session.add(user)
        db.session.commit()
                         
    
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

    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.Permissions is None:
            self.Permissions = 0

    def __repr__(self):
        return '<Role {}>'.format(self.Name)
    
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
    CREATE = 2
    EDIT = 4
    DELETE = 8
    ADMIN = 16
       
class Note(db.Model):
    __tablename__ = 'note'
    NoteId = db.Column(db.Integer,primary_key=True)
    CustomerId = db.Column(db.Integer,db.ForeignKey('customer.CustomerId'))
    AgentId = db.Column(db.Integer,db.ForeignKey('user.UserId'))
    Note = db.Column(db.String(2000))
    DateCreated = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Note {}>'.format(self.name)