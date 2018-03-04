# coding:utf8
from . import admin
from flask import abort, request, redirect, url_for
from flask_admin import expose, BaseView
from flask_admin.contrib.mongoengine import ModelView
from app.extensions import login_required, current_user
#from flask_admin.
from app.models import User, Wallet


#class Admin_View(BaseView):
#    @expose('/')
#    def index(self):
#        return self.render('admin/index.html')


class CRUD(ModelView):
    column_searchable_list = (User.username,)
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.role == 'admin':
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return self.login()
                #return redirect(url_for('admin.index', next=request.url))

    #def __init__(self, session, **kwargs):
     #   super(CRUD, self).__init__(User, session, **kwargs)

    @expose('/')
    @login_required
    def user(self):
        return self.render('admin/login.html')

    @expose('/login')
    def login(self):
        return self.render('admin/login.html')
