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
