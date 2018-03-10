from . import doctor
from flask import render_template, request, flash, redirect
from app.models import User, Commodity, Orders, Notice, DateDiag, DiagnosisLog
from app.extensions import login_required, current_user
from flask_admin.contrib.mongoengine.filters import ObjectId
from app.doctor.forms import NoticeForm, FinishDiagForm


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


@doctor.route('/diag_done')
@login_required
def diag_done():
    diags = DiagnosisLog.objects(doctor=current_user.realname)
    return render_template('doctor/diag_done.html', diags=diags)


@doctor.route('/wait_diag')
@login_required
def wait_diag():
    diags = DateDiag.objects(doctor=ObjectId(current_user.id), status=False)
    return render_template('doctor/wait_diag.html', diags=diags)


@doctor.route('/finish_diag/<diag_id>', methods=['POST', 'GET'])
@login_required
def finish_diag(diag_id):
    diag = DateDiag.objects(id=ObjectId(diag_id)).first()
    form = FinishDiagForm()
    print(diag.user_id.id)
    print(type(diag.user_id.id))
    if request.method == 'POST':
        diagnosis_result = form.diagnosis_result.data
        need_hospitalization = form.need_hospitalization.data
        need = True if need_hospitalization == 'yes' else False
        log = DiagnosisLog(diagnosis_result=diagnosis_result,
                           doctor=current_user.username,
                           custom=diag.user_id.username,
                           need_hospitalization=need,
                           user_id=diag.user_id.id,
                           for_dated=diag)
        log.save() and diag.update(status=True)
        flash('确认就诊成功！')
        return redirect('/doctor')
    return render_template('doctor/finish_diag.html', form=form, diag=diag)
