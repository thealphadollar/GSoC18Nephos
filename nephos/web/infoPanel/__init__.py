from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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

    from infoPanel.main import main_bp
    APP.register_blueprint(main_bp)

    return APP
