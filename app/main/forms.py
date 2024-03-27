from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateUserForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    role = SelectField('Role', validate_choice=False, coerce=int)

    submit = SubmitField('Submit')

class EditUserForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    role = SelectField('Role', validate_choice=False, coerce=int)

    submit = SubmitField('Submit')

class CreateCustomerForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    product = SelectField('Product', choices=[('1','Debtsolv'),('2','Wallkat'),('3','Training'),('4','Migration'),('5','Bespoke')],validators=[DataRequired()])
    description = StringField('Description')
    status = SelectField('Status', choices=[('New Lead','New Lead'),('Active','Active'),('Inactive','Inactive')],validators=[DataRequired()])
    contactname = StringField('Contact Name')
    contactemail = StringField('Contact Email',validators=[DataRequired()])
    contactphone = StringField('Contact Phone')
    agent = SelectField('Agent', validate_choice=False, coerce=int)
    submit = SubmitField('Submit')

class CreateRoleForm(FlaskForm):
    name = StringField('Name')
    permissions = SelectMultipleField('Permissions', choices=[('1','View'),('2','Create'),('4','Edit'),('8','Delete'),('16','Admin')],validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateNoteForm(FlaskForm):
    note = TextAreaField('Note')
    submit = SubmitField('Submit')