from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, URL


class InfoForm(Form):
    realname = StringField('realName', [DataRequired(), Length(max=100)])
    email = StringField('Email', [DataRequired(), Length(max=100)])
    idcard = StringField('idcard', [DataRequired(), Length(max=100)])
    bankcard = StringField('bankcard', [DataRequired(), Length(max=100)])
    location = StringField('location', [DataRequired(), Length(max=100)])
    tel = StringField('Phone', [DataRequired(), Length(max=100)])
    gander = BooleanField('gender')
