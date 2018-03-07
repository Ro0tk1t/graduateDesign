from . import doctor
from flask import render_template
from app.models import User, Commodity, Orders
from app.extensions import login_required, current_user
from flask_admin.contrib.mongoengine.filters import ObjectId

@doctor.route('/')
@login_required
def index():
    return render_template('home/user.html')

@doctor.route('/orders')
@login_required
def order():
    orders = Orders.objects(opareteUser=current_user.realname)
    drugs = {}
    for x in orders:
        for y in x.buyDetail:
            drugs[y] = Commodity.objects(id=ObjectId(y)).first().name
    return render_template('doctor/order.html', orders=orders, bought=drugs)

@doctor.route('/aaaaaaa')
@login_required
def a():
    return render_template()