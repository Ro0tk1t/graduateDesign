from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired


class SelectDrug(FlaskForm):
    selected = BooleanField('status')
