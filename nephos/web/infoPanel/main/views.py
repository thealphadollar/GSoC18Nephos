"""
main/views.py

Controller Responsible for Handling the main page

"""

from flask import Flask, render_template, Response
from infoPanel.main import main_bp
from infoPanel import db
import json


@main_bp.route('/', methods=['GET'])
def homepage():
    """
    <url>/

    View that Renders the Homepage

    """
    return "Hello World!"


@main_bp.route('/api/channels', methods=['GET'])
def channels():
    """
    <url>/api/channels

    View that Returns the channel

    """
    data = db.session.execute('SELECT * FROM channels;')
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    return Response(json.dumps([dict(r) for r in data]), mimetype='application/json')


@main_bp.route('/channels', methods=['GET'])
def show_channels():
    """
    <url>/api/channels

    View that Returns the channel and displays them in a nice table

    """
    data = db.session.execute('SELECT * FROM channels;')
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    channels = [dict(r) for r in data]
    return render_template('channels.html', channels=channels)
