#!/usr/bin/python3
# coding=utf-8

from flask import render_template
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_principal import Permission, Principal, RoleNeed

Bcrypt = Bcrypt()
Bootstrap = Bootstrap()
SQLAlchemy = SQLAlchemy

login_manage = LoginManager()
login_manage.login_view = 'login'
login_manage.session_protection = 'Strong'
login_manage.login_message = '登录后可见 !  请登录'
login_manage.login_message_category = 'info'


@login_manage.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template("403.html")

principal = Principal()
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
doctor_permission = Permission(RoleNeed('doctor'))
