#!/usr/bin/python3
# coding=utf-8

from setuptools import setup, find_packages


setup(
        name='app',
        version='0.1',
        long_description=__doc__,
        include_package_data=True,
        author='rootkit',
        description='GraduateDesign',
        packages=find_packages(),
        install_requires=[
            'flask==2.3.2',
            'Flask-Admin>=1.5.0',
            'Flask-Bcrypt>=0.7',
            'Flask-Bootstrap>=3.3',
            'Flask-Login>=0.4',
            'flask-mongoengine==0.9.5',
            'Flask-SQLAlchemy==2.3.2',
            'Flask-WTF>=0.14',
            'mongoengine==0.15',
            'pymongo>=3.6',
            'Werkzeug>=0.14',
            'WTForms>=2.1'
            ],
        extras_require={}
        )
