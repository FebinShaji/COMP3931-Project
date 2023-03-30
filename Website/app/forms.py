from flask_wtf import Form
from wtforms import TextField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.validators import length

class Login(Form):
    Username = TextField('Username', validators=[DataRequired(), length(max=20)])
    Password = TextField('Password', validators=[DataRequired(), length(max=20)])
    Remember = BooleanField('Remember')

class Register(Form):
    FirstName = TextField('FirstName', validators=[DataRequired(), length(max=30)])
    Surname = TextField('Surname', validators=[DataRequired(), length(max=30)])
    Email = TextField('Email', validators=[DataRequired(), length(max=20)])
    Username = TextField('Username', validators=[DataRequired(), length(max=20)])
    Password = PasswordField('Password', validators=[DataRequired(), length(max=20)])
    Confirm_Password = PasswordField('Confirm_Password', validators=[DataRequired(), length(max=20)])