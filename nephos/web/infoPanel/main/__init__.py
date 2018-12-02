from flask import Blueprint
main_bp = Blueprint('main', __name__)

from infoPanel.main import views
