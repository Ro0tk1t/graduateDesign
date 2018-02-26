# coding:utf8
from . import home
from flask import abort, redirect, url_for, render_template, request
from app.extensions import current_user, login_required
from app.models import User, Wallet, Orders, Commodity, ShoppingCar
from .forms import InfoForm
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
        user = User.objects(username=current_user.username).first()
        print(user)
        user.update(
            realname=realname,
            email=email,
            tel=tel,
            location=location,
            idCard=idcard,
            bindBankCard=bankcard
        )
        # flash('afdfd')
        return redirect('/home/{}/info'.format(current_user))
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
    orders = wallet.orders
    print(orders)
    return render_template('home/order.html', orders=orders)


@home.route('/pwd', methods=['POST', 'GET'])
def pwd():
    return render_template('home/pwd.html')


@home.route('/test1', methods=['POST', 'GET'])
def test1():
    return render_template('home/user.html')
