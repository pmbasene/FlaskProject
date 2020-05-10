from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators = [DataRequired(), Length(min=2, max=20)])
    email =  EmailField('Email',
                            validators = [DataRequired(), Email()])

    password =  PasswordField( 'Password', validators = [DataRequired()])
    confirm_password =  PasswordField( 'Confirm Password',
                            validators = [DataRequired(), EqualTo('password')])  
    submit = SubmitField('Sign up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. please choose an another one!')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is taken. please choose an another one!')

class LoginForm(FlaskForm):
 
    email =  StringField( 'Email',
                            validators = [DataRequired(), Email()])
    password =  PasswordField( 'Password', validators = [DataRequired()])    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign up')