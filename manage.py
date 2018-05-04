# coding:utf8
from app import create_app
from app.models import mongo, User
from flask import Flask
from flask_script import Shell, Manager

sh = Flask(__name__)
manager = Manager(sh)




@manager.shell
def make_shell_content():
    return dict(app=create_app(), db=mongo, user=User)


@manager.shell
def server():
    #app.debug = True
    create_app().run('0.0.0.0')


manager.add_command('shell', Shell(make_context=make_shell_content))
manager.add_command('server', server())
if __name__ == "__main__":
    manager.run()
