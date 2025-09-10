from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from app1 import Users

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LoadMoneyForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Load Money')

class SendMoneyForm(FlaskForm):
    username = StringField('Recipient Username', validators=[DataRequired(), Length(min=2, max=20)])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Send Money')
