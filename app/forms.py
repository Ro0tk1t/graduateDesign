#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length,EqualTo, URL
from flask import Flask
from app.models import User, Tag
from app import config

app = Flask(__name__)
#app.config.from_object('config')
class SearchForm(FlaskForm):
    keyword = StringField('KW', [DataRequired(), Length(max=100)])


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=100)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')


class RegistForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=100)])
    password = PasswordField('Password', [DataRequired()])
    # nikename = StringField('Username', [DataRequired(), Length(max=100)])
    email = StringField('Email', [DataRequired(), Length(max=100)])
    idcard = StringField('IDcard', [DataRequired(), Length(max=100)])
    bankcard = StringField('Bankcard', [DataRequired(), Length(max=100)])
    location = StringField('Locat', [DataRequired(), Length(max=100)])
    tel = StringField('Phone', [DataRequired(), Length(max=100)])


#    def check_pass(self):
#        cp = super(LoginForm, self).check_pass()
#        if not cp:
#            return False
#
#        user = User.query.filter_by(
#                username = self.username.data
#                ).first()
#        if not user:
#            self.username.errors.append(
#                    'Invalid username or password'
#                    )
#            return False
#
#        if not self.user.check_password():pass
