#! /usr/bin/python3
# coding:utf8
from flask import Flask, request, render_template
from flask import abort, redirect, flash, current_app
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
from app.drug import drug as drug_blueprint
from app.doctor import doctor as doctor_blueprint
from app.extensions import Bcrypt, Bootstrap, login_manage, principal, current_user, login_user, logout_user, admin_permission, login_required
from flask_principal import identity_changed, identity_loaded, UserNeed, RoleNeed, Identity, Permission
from flask_admin import Admin, BaseView
from flask_admin.contrib.mongoengine.filters import ObjectId
from app.models import mongo, db, User, Orders, Commodity, Tag,\
    Notice, Wallet, Security, ScoreGood, ScoreOrder, ShoppingCar,\
    DiagnosisLog, DateDiag, HospitalizationLog, Baoxian, Baoxian_order
from app.forms import LoginForm, SearchForm, RegistForm
from app import config
from .admin import views as admin_views
from datetime import timedelta,datetime
from os import path
from app.utils.pay import Alipay


def create_app(object_name=None):
    app = Flask(__name__)
    app.register_blueprint(home_blueprint, url_prefix='/home')
    app.register_blueprint(drug_blueprint, url_prefix='/drug')
    app.register_blueprint(doctor_blueprint, url_prefix='/doctor')
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')
    Bcrypt.init_app(app)
    Bootstrap.init_app(app)
    login_manage.init_app(app)
    principal.init_app(app)
    app.config.from_object(config.Config)


    admin = Admin(app, name='后台')
    model_list = [User, Orders, Commodity, Tag, Notice, Wallet, Security,
                  ScoreGood, ScoreOrder, ShoppingCar, DiagnosisLog,
                  DateDiag, HospitalizationLog, Baoxian, Baoxian_order]
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
            if user.role == 'doctor':
                return redirect('/doctor')
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
    @login_required
    def search():
        form = SearchForm()
        if request.method == 'POST':
            keyword = form.keyword.data
            drugs = Commodity.objects(tags__contains=keyword)
            if drugs:
                return render_template('chufang.html', drugs=drugs)
            else:
                flash('No drug found !')
                return render_template('chufang.html')
        return render_template('index.html')

    @app.route('/notice')
    def notice():
        notes = Notice.objects.all()
        return render_template('notice.html', notes=notes)

    @app.route('/scoreshop')
    def scoreshop():
        goods = ScoreGood.objects.all()
        return render_template('scoreshop.html', goods=goods)

    @app.route('/exchange/<good_id>')
    @login_required
    def exchange(good_id):
        good = ScoreGood.objects(id=good_id).first()
        need_score = good.score
        wallet = current_user.wallet_id
        have_score = wallet.score
        if have_score >= need_score:
            score_order = ScoreOrder(
                exchange=good,
                user_id=User.objects(id=current_user.id).first(),
                wallet_id=wallet.id,
                useScore=need_score
            )
            # TODO: 事务回滚
            score_order.save() and wallet.update(score=have_score-need_score)
            status = 1
        else:
            status = 0
        return render_template('exchange.html', status=status)

    @app.route('/test')
    @admin_permission.require(http_exception=403)
    def test():
        permission = Permission()
        return 'test admin permission'

    @app.template_filter('compute_price')
    def compute_price(drug_dict):
        ''' 自定义的jinjia2过滤器,用于计算购物车商品总价 '''
        price = 0.0
        for k,v in drug_dict.items():
            price += k.price * v
        return price

    @app.route('/baoxian')
    def baoxian():
        baoxian_list = Baoxian.objects().all()
        return render_template('baoxian/baoxian.html', baoxian_list=baoxian_list)

    @app.route('/baoxian_introduce/<id>')
    def baoxian_introduce(id):
        baoxian_obj = Baoxian.objects(id=ObjectId(id)).first()
        return render_template('baoxian/baoxian_introduce.html', baoxian=baoxian_obj)

    @app.route('/')
    def ali_pay():
        app_id = "2016091500513426"
        notify_url = 'http://localhost:5000/'
        return_url = 'http://localhost:5000/'
        priv_key_path = path.join(path.dirname(path.abspath(__file__)), 'zfb_priv_key.pem')
        pub_key_path = path.join(path.dirname(path.abspath(__file__)), 'zfb_pub_key.pem')
        alipay = Alipay(app_id=app_id,
                        app_notify_url=notify_url,
                        return_url=return_url,
                        app_private_key_path=priv_key_path,
                        alipay_public_key_path=pub_key_path,
                        debug=True)
        return alipay


    return app

#if __name__ == '__main__':
#    create_app().run(host='0.0.0.0', debug=False)
