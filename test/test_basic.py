#!/usr/bin/python3
# coding=utf-8

import unittest
from flask import current_app
from app import create_app, db, config

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertTrue(current_app)

    def test_config_CSRF(self):
        self.assertTrue(config.Config.CSRF_ENABLED)

    def test_config_db_connect(self):
        self.assertIsNotNone(config.DevConfig.MONGODB_SETTINGS)
        self.assertIsInstance(config.DevConfig.MONGODB_SETTINGS, dict)

