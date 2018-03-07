# coding:utf8
from flask import Blueprint

doctor = Blueprint('doctor', __name__)

import app.doctor.views
