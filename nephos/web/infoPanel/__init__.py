from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='static')
db = SQLAlchemy()

basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '../../databases/storage.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'nesho'

db = SQLAlchemy(app)


def create_app():
    db.init_app(app)

    from infoPanel.main import main_bp
    app.register_blueprint(main_bp)

    return app
