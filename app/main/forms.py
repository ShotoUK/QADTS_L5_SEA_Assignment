from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateUserForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    role = SelectField('Role', choices=[('1','Admin'),('2','User'),('3','Agent')])

    submit = SubmitField('Submit')

class CreateCustomerForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    product = SelectField('Product', choices=[('1','Debtsolv'),('2','Wallkat'),('3','Training'),('4','Migration'),('5','Bespoke')],validators=[DataRequired()])
    description = StringField('Description')
    status = SelectField('Status', choices=[('New Lead','New Lead'),('Active','Active'),('Inactive','Inactive')],validators=[DataRequired()])
    contactname = StringField('Contact Name')
    contactemail = StringField('Contact Email',validators=[DataRequired()])
    contactphone = StringField('Contact Phone')
    agent = SelectField('Agent', choices=[('1','Charlton'),('2','Jeff'),('3','Jim'),('4','Barry'),('5','Jess')])
    submit = SubmitField('Submit')

class CreateRoleForm(FlaskForm):
    name = StringField('Name')
    permissions = SelectMultipleField('Permissions', choices=[('1','View'),('2','Edit'),('4','Admin')])
    submit = SubmitField('Submit')

class CreateNoteForm(FlaskForm):
    note = TextAreaField('Note')
    submit = SubmitField('Submit')