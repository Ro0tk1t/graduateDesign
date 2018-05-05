# coding:utf8
from datetime import datetime
from flask import Flask
from app.extensions import Bcrypt, SQLAlchemy
from flask_login import AnonymousUserMixin
from flask_mongoengine import MongoEngine
from app import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)
db = SQLAlchemy(app)
mongo = MongoEngine(app)


#class Role(mongo.Document):
#    name = mongo.StringField()
#    description = mongo.StringField(default='user')
#
#    def __repr__(self):
#        return '<Role %r' % self.name

role_list = ('admin', 'user', 'doctor')

class User(mongo.Document):
    ''' 用户 '''
    username = mongo.StringField(required=True, unique=True)
    realname = mongo.StringField()
    password = mongo.StringField()
    email = mongo.StringField(unique=True)
    gender = mongo.BooleanField()
    tel = mongo.StringField(unique=True)
    idCard = mongo.StringField(unique=True)
    bindBankCard = mongo.StringField(unique=True)
    location = mongo.StringField()
    joinTime = mongo.DateTimeField(default=datetime.now)
    lastLogin = mongo.DateTimeField(default=datetime.now)
    #user_role = mongo.Re('Role', secondary=Roles, backref=db.backref('users', lazy='dynamic'))
    role = mongo.StringField(choices=role_list)
    wallet_id = mongo.ReferenceField('Wallet')
    shoppingcar = mongo.ReferenceField('ShoppingCar')
    security = mongo.ReferenceField('Security')

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def encrypt_password(self, password):
        self.password = str(Bcrypt.generate_password_hash(password))

    def check_password(self, password):
            return Bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return self.username


class Wallet(mongo.Document):
    ''' 钱包 '''
    surplus = mongo.FloatField(default=0.0)
    score = mongo.IntField(default=0)
    tongchoujijin = mongo.FloatField(default=0.0)
    orders = mongo.ListField(mongo.ReferenceField('Orders'))

    def __repr__(self):
        return '<Wallet %r>' % self.id


class ShoppingCar(mongo.Document):
    ''' 购物车 '''
    detail = mongo.DictField()


class Orders(mongo.Document):
    ''' 订单 '''
    createDate = mongo.DateTimeField(default=datetime.now)
    user_id = mongo.ReferenceField(User)
    opareteUser = mongo.StringField(default='President')
    useTongchou = mongo.FloatField(default=0.0)
    payWay = mongo.StringField(default='余额')
    buyDetail = mongo.DictField()
    #buyDetail = db.relationship('Commodity', secondary=Commodities, backref=db.backref('orders', lazy='dynamic'))
    isPayed = mongo.BooleanField(default=False)
    getScore = mongo.IntField(default=0)
    paySum = mongo.FloatField()
    wallet_id = mongo.ReferenceField(Wallet)

    def __repr__(self):
        return "<Orders %r>" % self.id

class Commodity(mongo.Document):
    ''' 药品 '''
    name = mongo.StringField()
    pic_name = mongo.StringField()
    price = mongo.FloatField(required=True)
    explain = mongo.StringField()
    tags = mongo.ListField(mongo.StringField())

    def __repr__(self):
        return '<Commodity %r>' % self.name



class ScoreGood(mongo.Document):
    ''' 积分商品 '''
    name = mongo.StringField()
    score = mongo.IntField(required=True)
    equalRMB = mongo.FloatField()
    pic_name = mongo.StringField()
    onlineDate = mongo.DateTimeField(default=datetime.now)

    def __repr__(self):
        return '<ScoreGood %r>' % self.name


class ScoreOrder(mongo.Document):
    ''' 积分订单 '''
    exchange = mongo.ReferenceField(ScoreGood)
    createDate = mongo.DateTimeField(default=datetime.now)
    user_id = mongo.ReferenceField(User)
    wallet_id = mongo.ReferenceField(Wallet)
    useScore = mongo.IntField()

    def __repr__(self):
        return '<ScoreOrder %r' % self.id


class Tag(mongo.Document):
    ''' 商品标签 '''
    title = mongo.StringField(unique=True)
    drugs = mongo.ListField(mongo.ReferenceField('Commodity'))
    #drugs = db.relationship('Commodity', secondary=Tags, backref=db.backref('tag', lazy='dynamic'))

    def __repr__(self):
        return '<Tag %r>' % self.title


class Security(mongo.Document):
    ''' 密保 '''
    question = mongo.StringField()
    answer = mongo.StringField()
    user_id = mongo.ReferenceField(User)

    def __repr__(self):
        return "<Security %r>" % self.id


class Notice(mongo.Document):
    ''' 公告 '''
    title = mongo.StringField()
    text = mongo.StringField()
    addDate = mongo.DateTimeField(default=datetime.now)


class DiagnosisLog(mongo.Document):
    ''' 诊断记录 '''
    user_id = mongo.ReferenceField('User')
    diagnosis_date = mongo.DateTimeField(default=datetime.now)
    doctor = mongo.StringField(default='admin')
    custom = mongo.StringField()  # 患者姓名
    diagnosis_result = mongo.StringField(default='healthy')
    need_hospitalization = mongo.BooleanField()
    for_dated = mongo.ReferenceField('DateDiag')


class DateDiag(mongo.Document):
    ''' 预约记录 '''
    user_id = mongo.ReferenceField('User')
    date = mongo.DateTimeField()
    create_date = mongo.DateTimeField(default=datetime.now)
    status = mongo.BooleanField(default=False)
    custom = mongo.StringField()   #患者姓名
    doctor = mongo.ReferenceField('User')
    about_me = mongo.StringField()


class HospitalizationLog(mongo.Document):
    ''' 住院记录 '''
    user_id = mongo.ReferenceField('User')
    id_card = mongo.StringField()
    start_date = mongo.DateTimeField(default=datetime.now)
    status = mongo.BooleanField(default=True)
    end_date = mongo.DateTimeField()
    place = mongo.StringField(required=True)

# class News(db.Model):
#    auth = db.relationship("User", backref='news')
#    pushDate = mongo.DateTimeField(default=datetime.now)
#    title = mongo.StringField(db.Text)
#    context = mongo.StringField(db.Text)
#
#    def __repr__(self):
#        return "<News %r>" % self.id

#u = User(username='admin', password='admin')
#w = Wallet(surplus=100, score=100, tongchoujijin=100, user_id=u)
#db.session.add(u)
#db.session.add(w)
#db.session.commit()

#test

#notice = Notice()
#notice.title = 'fuck'
#notice.text = 'society'
#notice.save()

#db.drop_all()
#db.create_all()

#import os
#os.chdir('/home/rootkit/PycharmProjects/app/app/static/pic/drug')
#for x in os.listdir():
#    print(x)
#    if os.path.isfile(x):
#        d = Commodity(pic_name=x, price=250)
#        print(d)
#        d.save()
#    else:
#        print(x + '  is dir')
