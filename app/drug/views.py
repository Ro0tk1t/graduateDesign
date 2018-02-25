# coding:utf8

from . import drug
from flask import abort, redirect, url_for, render_template, request
from app.extensions import current_user, login_required
from app.models import Commodity

@drug.route('/')
@login_required
def index():
    drugs = Commodity.objects.all()
    print(type(drugs))
    print(drugs)
    print(dir(drugs))
    return render_template('chufang.html', drugs=drugs)


@drug.route('login')
def login():
    redirect('login')
