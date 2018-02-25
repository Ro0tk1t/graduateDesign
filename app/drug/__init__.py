# coding:utf8
from flask import Blueprint

drug = Blueprint('drug', __name__)

import app.drug.views