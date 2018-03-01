from flask_wtf import Form
from app.models import User
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, DateTimeField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, URL
# validators里是验证函数，把一个字段绑定某个验证函数之后，flask会在接收表单中的数据之前对数据做一个验证，如果验证成功才会接收数据。


class InfoForm(Form):
    realname = StringField('realName', [DataRequired(), Length(max=100)])
    email = StringField('Email', [DataRequired(), Length(max=100)])
    idcard = StringField('idcard', [DataRequired(), Length(max=100)])
    bankcard = StringField('bankcard', [DataRequired(), Length(max=100)])
    location = StringField('location', [DataRequired(), Length(max=100)])
    tel = StringField('Phone', [DataRequired(), Length(max=100)])
    gander = BooleanField('gender')


class DateDiagnosis(Form):
    docs = User.objects(role='doctor')
    li = []
    for x in docs:
        li.append((x.id, x.realname))
    print(li)
    date = DateTimeField("预约时间", format="%Y-%m-%d %H:%M:%S")
    doctor = SelectField('预约医生', choices=li)
    about = TextAreaField('病情描述')