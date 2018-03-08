from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class NoticeForm(FlaskForm):
    title = StringField('title', [DataRequired(), Length(max=100)])
    content = TextAreaField('content', [DataRequired()])

class FinishDiagForm(FlaskForm):
    diagnosis_result = TextAreaField('result', [DataRequired()])
    need_hospitalization = StringField('hospitalization', [DataRequired()])
