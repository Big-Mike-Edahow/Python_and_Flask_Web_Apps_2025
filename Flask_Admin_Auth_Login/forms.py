# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember me: ', default='checked')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    submit = SubmitField('Register')
