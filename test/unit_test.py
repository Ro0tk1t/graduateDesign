#!/usr/bin/python3
# coding=utf-8

import unittest
import tempfile

class TestConfig():
    DEBUG = True
    DEBUG_TB_ENABLED = False
    DB = 'node'
    HOST = 'localhost'
    PORT = 27017
    SQLALCHEMY_DATABASE_URI = 'mongodb://%s:%d/%s' % (HOST, PORT, DB)
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLES = False

