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

class Workout(Form):
    Name = TextField('Name', validators=[DataRequired(), length(max=20)])
    Type = TextField('Type', validators=[DataRequired(), length(max=20)])

class Exercise(Form):
    ExerciseName = TextField('ExerciseName', validators=[DataRequired(), length(max=50)])

class Weights(Form):
    Date = DateField('Date', validators=[DataRequired(), length(max=20)])
    Set1 = TextField('Set1', validators=[DataRequired(), length(max=20)])
    Set2 = TextField('Set2', validators=[DataRequired(), length(max=20)])
    Set3 = TextField('Set3', validators=[DataRequired(), length(max=20)])
    Set4 = TextField('Set4', validators=[DataRequired(), length(max=20)])