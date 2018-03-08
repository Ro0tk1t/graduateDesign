from . import doctor
from flask import render_template, request, flash
from app.models import User, Commodity, Orders, Notice
from app.extensions import login_required, current_user
from flask_admin.contrib.mongoengine.filters import ObjectId
from app.doctor.forms import NoticeForm

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

@doctor.route('/add_notice', methods=['POST', 'GET'])
@login_required
def add_notice():
    form = NoticeForm()
    if request.method == 'POST':
        title = form.title.data
        content = form.content.data
        notice = Notice(title=title, text=content)
        notice.save() and flash('添加公告成功！')
        return render_template('doctor/add_notice.html', form=form)
    return render_template('doctor/add_notice.html', form=form)
