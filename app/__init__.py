#! /usr/bin/python3
# coding:utf8
from flask import Flask, request, render_template
from flask import abort, redirect, flash, current_app
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
from app.drug import drug as drug_blueprint
from app.extensions import Bcrypt, Bootstrap, login_manage, principal, current_user, login_user, logout_user, admin_permission
from flask_principal import identity_changed, identity_loaded, UserNeed, RoleNeed, Identity, Permission
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.contrib.mongoengine.view import BaseModelView
from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter
from app.models import mongo, db, User, Orders, Commodity, Tag, Notice, Wallet, Security, ScoreGood, ScoreOrder, ShoppingCar,DiagnosisLog, DateDiag
from app.forms import LoginForm, SearchForm, RegistForm
from app import config
from .admin import views as admin_views
from datetime import timedelta,datetime


app = Flask(__name__)
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(drug_blueprint, url_prefix='/drug')
# app.register_blueprint(admin_blueprint, url_prefix='/admin')
Bcrypt.init_app(app)
Bootstrap.init_app(app)
login_manage.init_app(app)
principal.init_app(app)
app.config.from_object(config.Config)


admin = Admin(app, name='后台')
model_list = [User, Orders, Commodity, Tag, Notice, Wallet, Security, ScoreGood, ScoreOrder, ShoppingCar, DiagnosisLog, DateDiag]
for x in model_list:
    admin.add_view(admin_views.CRUD(x, db.session, category=x.__name__))

# 会话到期时间
#app.permanent_session_lifetime = timedelta(minutes=30)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.role:
            identity.provides.add(RoleNeed(role.name))


# 身份认证

@login_manage.user_loader
def load_user(userid):
    return User.objects(id=userid).first()


@app.errorhandler(404)
def page404(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page500(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if hasattr(current_user, 'id'):
        user = current_user
    else:
        user = 'Guest'
    return render_template('index.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # name = request.form.get('username')
        name = form.username.data
        print(name)
        pwd = request.form.get('password')
        user = User.objects(username=name, password=pwd).first()
        if not user:
            return render_template('login.html', form=form, status=1)
        ### type(ObjectId) != type(str)
        user.id = str(user.id)
        login_user(user, remember=form.remember.data)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )
        flash('login success !', category='login success')
        user.update(lastLogin=datetime.now)
        if user.role == 'admin':
            return redirect('/admin')
        return redirect('/home')
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('login')


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        email = form.email.data
        idcard = form.idcard.data
        bankcard = form.bankcard.data
        location = form.location.data
        tel = form.tel.data
        wallet = Wallet()
        shop = ShoppingCar()
        customer = User(username=username,
                        email=email,
                        password=password,
                        idCard=idcard,
                        bindBankCard=bankcard,
                        location=location,
                        role='user',
                        wallet_id=wallet,
                        shoppingcar=shop,
                        tel=tel)
        #customer.encrypt_password(password)
        wallet.save() and shop.save() and customer.save()
        flash('注册成功 !')
        return redirect('/')
    return render_template('regist.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    drugs = Commodity.objects(tag=form.keyword.data)
    print(drugs)
    if request.method == 'POST':
        return '<h1>Search for {}</h1>'.format(drugs)


@app.route('/notice')
def notice():
    notes = Notice.objects.all()
    return render_template('notice.html', notes=notes)


@app.route('/scoreshop')
def scoreshop():
    return render_template('scoreshop.html')

@app.route('/test')
@admin_permission.require(http_exception=403)
def test():
    permission = Permission()
    return 'test admin permission'

# if __name__ == '__main__':
#    app.run(host='0.0.0.0',debug=False)
