from . import doctor
from flask import render_template, request, flash
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
    diags = DateDiag.objects(doctor=ObjectId(current_user.id))
    return render_template('doctor/wait_diag.html', diags=diags)

@doctor.route('/finish_diag/<diag_id>', methods=['POST', 'GET'])
@login_required
def finish_diag(diag_id):
    diag = DateDiag.objects(id=ObjectId(diag_id))
    form = FinishDiagForm()
    if request.method == 'POST':
        diagnosis_result = form.diagnosis_result.data
        need_hospitalization = form.need_hospitalization.data
        DiagnosisLog(diagnosis_result=diagnosis_result,
                     need_hospitalization=need_hospitalization,
                     doctor=current_user.realname,
                     custom=User.objects(id)    ##########################################################################################    WIP
                     )
    return render_template('doctor/finish_diag.html')