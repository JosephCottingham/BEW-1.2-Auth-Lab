from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from books_app.models import User

class SignUpForm(FlaskForm):
    username = StringField('Username', required=True)
    password = StringField('Password', required=True)
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', required=True)
    password = StringField('Password', required=True)
    submit = SubmitField('Submit')
