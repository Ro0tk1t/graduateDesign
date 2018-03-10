# coding:utf8
from . import home
from flask import abort, redirect, url_for, render_template, request, flash
from app.extensions import current_user, login_required
from app.models import User, Orders, Commodity, DiagnosisLog, DateDiag, HospitalizationLog
from .forms import InfoForm, DateDiagnosis, PwdForm
from flask_admin.contrib.mongoengine.filters import ObjectId
from collections import Counter
from functools import reduce


@home.route("/")
@home.route("/<user>")
@login_required
def index(user=0):
    if current_user.is_authenticated:
        if user:
            user = User.objects(username=user).first()
            if not user:
                return '此用户不存在 !'
            return render_template('home/user.html', user=user)
        else:
            user = current_user
            return render_template('home/user.html', user=user)
    else:
        return 'please login'


@home.route('/<user>/info', methods=['POST', 'GET'])
@login_required
def info(user):
    return render_template('home/info.html', user=user)


@home.route('/change_info', methods=['POST', 'GET'])
@login_required
def change_info():
    form = InfoForm()
    if request.method == 'POST':
        realname = form.realname.data
        email = form.email.data
        tel = form.tel.data
        location = form.location.data
        idcard = form.idcard.data
        bankcard = form.bankcard.data
        gender = form.gender.data
        gender = gender == 'men'
        user = User.objects(username=current_user.username).first()
        print(user.__repr__())
        user.update(
            realname=realname,
            email=email,
            tel=tel,
            location=location,
            idCard=idcard,
            bindBankCard=bankcard,
            gender=bool(int(gender))
        )
        flash('个人资料修改成功 !')
        return redirect('/home'.format(current_user))
    else:
        return render_template('home/edit_info.html')


@home.route('/money')
@login_required
def money():
    user_wallet = current_user.wallet_id
    return render_template('home/money.html', wallet=user_wallet)


@home.route('/add/<commodity>', methods=['POST', 'GET'])
@login_required
def add(commodity):
    ''' 添加到购物车 '''
    commodity_objid = ObjectId(commodity)
    selected = Commodity.objects(id=commodity_objid).first()
    print(commodity_objid)
    user = User.objects(id=ObjectId(current_user.id)).first()
    user.shoppingcar.update(push__detail={str(selected.id): 1})
    return render_template('home/pay.html')

@home.route('/pay/null')
@home.route('/pay/<goods>', methods=['POST', 'GET'])
@login_required
def pay(goods):
    ''' jinja2只能返回str,无法返回对象或列表等数据结构 '''
    drug = goods.split(',')
    drugs = [Commodity.objects(id=ObjectId(x.strip())).first() for x in drug]
    need_pay = sum([x.price for x in drugs])
    detail = Counter(drug)
    print(detail)
    user = User.objects(id=current_user.id).first()
    wallet = current_user.wallet_id
    print(drugs)
    order = Orders(user_id=user,
                   buyDetail=detail,
                   paySum=need_pay,
                   wallet_id=wallet)
    order.save()
    '''
    检查是否已经支付
    '''
    current_user.shoppingcar.update(detail={})
    return render_template('home/pay.html')


@home.route('/shopping_car')
@login_required
def shopping_car():
    goods = current_user.shoppingcar.detail
    ids = []
    for x in goods:
        # 字符串id转化为药品对象并追加到药品列表
        ids.append(Commodity.objects(id=ObjectId(list(x.keys())[0])).first())
    return render_template('home/car.html', goods=ids)


@home.route('/delete/<commodities>')
@login_required
def delete(commodities):
    pass


@home.route('/order')
@login_required
def order():
    wallet = current_user.wallet_id
    #orders = wallet.orders
    orders = Orders.objects(wallet_id=wallet)
    drugs = {}
    for x in orders:
        for y in x.buyDetail:
            drugs[y] = Commodity.objects(id=ObjectId(y)).first().name
    return render_template('home/order.html', orders=orders, bought=drugs)


@home.route('/pwd', methods=['POST', 'GET'])
def pwd():
    form = PwdForm()
    if request.method == 'POST':
        old_pwd = form.old_pwd.data
        new_pwd = form.new_pwd.data
        user = User.objects(id=ObjectId(current_user.id)).first()
        print(user.password)
        if user.password == old_pwd:
            user.update(password=new_pwd)
            flash('密码修改成功 ！')
            return redirect('/home')
        else:
            return render_template('home/pwd.html', status=1)
    return render_template('home/pwd.html')


@home.route('/tongchoujijin')
@login_required
def tongchoujijin():
    wallet = current_user.wallet_id
    jijin = wallet.tongchoujijin
    return render_template('home/tongchoujijin.html', jijin=jijin)


@home.route('/used_jijin')
@login_required
def usejijin():
    wallet = current_user.wallet_id
    jijin_order = Orders.objects(wallet_id=wallet, useTongchou__gt=0)
    drugs = {}
    for x in jijin_order:
        for y in x.buyDetail:
            drugs[y] = Commodity.objects(id=ObjectId(y)).first().name
    return render_template('home/jijin_order.html',
                           jijin_order=jijin_order,
                           bought=drugs)


@home.route('/diagnosis')
@login_required
def diagnosis():
    diags = DiagnosisLog.objects(user_id=ObjectId(current_user.id))
    return render_template('home/diagnosis.html', diags=diags)


@home.route('/date_diag', methods=['POST', 'GET'])
@login_required
def date_diag():
    form = DateDiagnosis()
    if request.method == 'POST':
        date = form.date.data
        doctor = form.doctor.data
        about = form.about.data
        add = DateDiag(doctor=User.objects(id=ObjectId(doctor)).first(),
                       user_id=User.objects(id=ObjectId(current_user.id)).first(),
                       date=date, custom=current_user.username,
                       about_me=about)
        add.save()
        flash('预约成功!  ')
        return redirect('/home')
    return render_template('home/date_diag.html', form=form)


@home.route('/date_diag_list', methods=['POST', 'GET'])
@login_required
def date_diag_list():
    dates = DateDiag.objects(user_id=ObjectId(current_user.id))
    return render_template('home/date_diag_list.html', dates=dates)


@home.route('/one_diag/<log_id>', methods=['POST', 'GET'])
@login_required
def one_diag(log_id):
    date_log = DateDiag.objects(id=ObjectId(log_id)).first()
    check_log = DiagnosisLog.objects(for_dated=date_log.id).first()
    return render_template('home/one_diag.html', log=check_log)

@home.route('/hospitalization_log')
@login_required
def hospitalization_log():
    logs = HospitalizationLog.objects()
    return render_template('home/hospitalization_log.html', logs=logs)