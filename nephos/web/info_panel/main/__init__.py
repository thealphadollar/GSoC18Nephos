"""
Initialize the Handler for the main part
"""
from flask import Blueprint
MAIN_BP = Blueprint('main', __name__)

from info_panel.main import views
