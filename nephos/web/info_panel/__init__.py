import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__, static_folder='static')
DB = SQLAlchemy()

BASEDIR = os.path.dirname(os.path.abspath(__file__))
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASEDIR, '../../databases/storage.db')
APP.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

APP.config['SECRET_KEY'] = 'nesho'

DB = SQLAlchemy(APP)


def create_app():
    """
    Creates the Flask App and initializes it's views
    """
    DB.init_app(APP)

    from info_panel.main import MAIN_BP
    APP.register_blueprint(MAIN_BP)

    return APP
