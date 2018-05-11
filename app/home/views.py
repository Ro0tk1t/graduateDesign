# coding:utf8
from . import home
from flask import abort, redirect, url_for, render_template, request, flash
from app.extensions import current_user, login_required
from app.models import User, Orders, Commodity, DiagnosisLog, DateDiag, HospitalizationLog, ScoreOrder, Baoxian, Baoxian_order
from .forms import InfoForm, DateDiagnosis, PwdForm
from bson import ObjectId
from collections import Counter
from ast import literal_eval
from urllib import parse


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
    user = User.objects(id=ObjectId(current_user.id)).first()
    in_cars = user.shoppingcar.detail
    if commodity in in_cars:
        in_cars[commodity] += 1
    else:
        in_cars[commodity] = 1
    user.shoppingcar.update(detail=in_cars)
    return render_template('home/pay.html')


@home.route('/pay/null')
@home.route('/pay/<goods>', methods=['POST', 'GET'])
@login_required
def pay(goods):
    ''' jinja2只能返回str,无法返回对象或列表等数据结构 '''
    try:
        _ = parse.unquote(goods)
        drug = literal_eval(_)
        if not drug:
            return render_template('home/pay.html', status=0)
    except:
        return render_template('home/pay.html', status=0)
    need_pay = 0.0
    for k,v in drug.items():
        commodity = Commodity.objects(id=ObjectId(k)).first()
        need_pay += commodity.price * v
    user = User.objects(id=current_user.id).first()
    wallet = current_user.wallet_id
    have_surplus = wallet.surplus
    if have_surplus < need_pay:
        return render_template('home/pay.html', status=0)
    else:
        get_score = int(need_pay/10)
        have_score = wallet.score
        order = Orders(user_id=user,
                       buyDetail=drug,
                       paySum=need_pay,
                       getScore=get_score,
                       wallet_id=wallet)
        before_buy = current_user.shoppingcar.detail
        after_buy = {}
        for k,v in before_buy.items():
            if k in drug:
                amount = v - drug[k]
                if amount > 0:
                    after_buy[k] = amount
            else:
                after_buy[k] = v
        current_user.shoppingcar.update(detail=after_buy)
        order.save()
        wallet.update(score=get_score+have_score,
                      surplus=have_surplus-need_pay)
        # TODO: 事务回滚
    '''
    检查是否已经支付
    '''
    return render_template('home/pay.html', status=1)


@home.route('/shopping_car')
@login_required
def shopping_car():
    goods = current_user.shoppingcar.detail
    new_goods = {}
    for k,v in goods.items():
        # 字符串id转化为药品对象并追加到药品字典  /*列表*/
        new_goods[Commodity.objects(id=ObjectId(k)).first()] = v
    return render_template('home/car.html', goods=new_goods)


@home.route('/delete/<commodities>')
@login_required
def delete(commodities):
    try:
        _ = parse.unquote(commodities)
        drugs = literal_eval(_)
    except:
        return render_template('home/car.html', goods={})
    car = current_user.shoppingcar
    before_del = car.detail
    for k,v in drugs.items():
        if k in before_del:
            if v > 0 and v < before_del[k]:
                before_del[k] -= v
            elif v == before_del[k]:
                del(before_del[k])
    car.update(detail=before_del)


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


@home.route('/scoreorder')
@login_required
def score_order():
    orders = ScoreOrder.objects(user_id=current_user.id)
    return render_template('home/scoreorder.html', orders=orders)


@home.route('/havescore')
@login_required
def have_score():
    score = current_user.wallet_id.score
    return render_template('home/havescore.html', score=score)

@home.route('/pwd', methods=['POST', 'GET'])
@login_required
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
    logs = HospitalizationLog.objects(user_id=ObjectId(current_user.id))
    return render_template('home/hospitalization_log.html', logs=logs)


@home.route('/buy_baoxian/<id>')
def buy_baoxian(id):
    baoxian_obj = Baoxian.objects(id=ObjectId(id)).first()
    wallet = current_user.wallet_id
    price = baoxian_obj.price
    surplus = wallet.surplus
    tongchou = wallet.tongchoujijin
    have_score = wallet.score
    score = int(price/10)

    order = Baoxian_order(user_id=ObjectId(current_user.id),
                          wallet_id=wallet,
                          baoxian_id=baoxian_obj,
                          get_score=score,
                          money=price)
    if tongchou >= 0:
        if price <= tongchou:
            order.tongchoujijin = price
            wallet.update(tongchoujijin=tongchou - price,
                          score=have_score+score)
            order.tongchoujijin = price
            order.save()
            flash('购买成功 !')
            return render_template('home/user.html')
        other_pay = price - tongchou
        if other_pay <= surplus:
            wallet.update(tongchoujijin=0,
                          score=have_score + score,
                          surplus=surplus-other_pay)
            order.tongchoujijin = tongchou
            order.save()
            flash('购买成功 !')
    else:
        flash('余额不足......')
    return render_template('home/user.html')

@home.route('/list_baoxian_orders')
def list_baoxian_orders():
    baoxian_orders = Baoxian_order.objects(wallet_id=current_user.wallet_id)
    return render_template('baoxian/baoxian_orders.html', baoxian_orders=baoxian_orders)