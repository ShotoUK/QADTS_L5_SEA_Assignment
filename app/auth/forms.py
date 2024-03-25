from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Length(1,64)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('password2',message='Passwords must match')])
    password2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(Email=field.data).first():
            raise ValidationError('Email already registered.')
        
    def validate_username(self,field):
        if User.query.filter_by(Email=field.data).first():
            raise ValidationError('Username already in use.')
        
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')