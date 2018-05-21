#!/usr/bin/python3
# coding=utf-8

class Config(object):
    SECRET_KEY = 'e5895216f74869ce2768d7dc2244184a'
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    @staticmethod
    def init_app(app):
        pass


class DevConfig(object):
    MONGODB_SETTINGS = {
        'db': 'node',
        'host': 'localhost',
        'port': 27017
    }

    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_BACKEND = 'amqp://guest:guest@localhost:5672//'
