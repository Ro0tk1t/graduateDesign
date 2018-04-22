#!/usr/bin/python3
# coding=utf-8

import unittest
from flask import url_for
from test_basic import BasicTest

class Test_URL_Path(BasicTest):
    def setUp(self):
        super(Test_URL_Path, self).setUp()
    def tearDown(self):
        pass

    def test1(self):
        print('*******************************')
        #print(dir(self.app))

    def test_root(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data)

    def test_login_page(self):
        res = self.client.get('login')
        text = res.data.decode()
        self.assertIn('username', text)
        self.assertIn('password', text)

    def test_login(self):
        data = {'username': 'test',
                'password': 'test'}
        res = self.client.post('login', data=data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        res = self.client.get('logout')
        text = res.data.decode()
        self.assertEqual(res.status_code, 302)
        self.assertIn('<a href="login">login</a>', text)

    def test_drug(self):
        res = self.client.get('drug/', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('403', res.data.decode())
        self.assertIn('Permission Deny!', res.data.decode())

    def test_admin(self):
        res = self.client.get('admin/')
        data = res.data.decode()
        self.assertNotIn('User', data)
        self.assertNotIn('Wallt', data)
        self.assertNotIn('Orders', data)

    def test_user_home(self):
        res = self.client.get('home/test')
        data = res.data.decode()
        self.assertIn('403', res.data.decode())
        self.assertIn('Permission Deny!', res.data.decode())
