"""
    Form module
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.db_models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=10), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User already exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class SubmitQuoteForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Post')

class EditQuoteForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Save')