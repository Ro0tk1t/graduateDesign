from flask_wtf import Form
from wtforms import BooleanField
from wtforms.validators import DataRequired


class SelectDrug(Form):
    selected = BooleanField('status')
