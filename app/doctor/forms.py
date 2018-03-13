from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length


class NoticeForm(FlaskForm):
    title = StringField('title', [DataRequired(), Length(max=100)])
    content = TextAreaField('content', [DataRequired()])

class FinishDiagForm(FlaskForm):
    diagnosis_result = TextAreaField('result', [DataRequired()])
    need_hospitalization = StringField('hospitalization', [DataRequired()])
    username = StringField('username')


class HostForm(FlaskForm):
    realname = StringField('患者姓名', [DataRequired()])
    id_card = StringField('患者身份证号', [DataRequired()])
    #start_date = DateTimeField('开始时间', [DataRequired()])
    end_date = DateTimeField('预计结束时间', [DataRequired()])
    place = StringField('住院地点', [DataRequired()])
