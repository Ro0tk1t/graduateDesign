# coding:utf8

from . import drug
from flask import abort, redirect, url_for, render_template, request
from app.extensions import current_user, login_required
from app.models import Commodity
from flask_admin.contrib.mongoengine.filters import ObjectId

@drug.route('/')
@login_required
def index():
    drugs = Commodity.objects.all()
    return render_template('chufang.html', drugs=drugs)


@drug.route('login')
def login():
    redirect('login')


@drug.route('/drug_info/<id>')
def drug_info(id):
    if not current_user.is_authenticated:
        abort(403)
    drug = Commodity.objects(id=ObjectId(id)).first()
    print(drug)
    return render_template('drug_info.html', drug=drug)
