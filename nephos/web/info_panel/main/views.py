"""
main/views.py

Controller Responsible for Handling the main page

"""
import json
from flask import render_template, Response, redirect, url_for, flash
from ..main import MAIN_BP
from ..main.forms import edit_channel_form, delete_form, channel_form
from .. import DB



@MAIN_BP.route('/', methods=['GET'])
def homepage():
    """
    <url>/

    View that Renders the Homepage

    """
    return "Hello World!"


@MAIN_BP.route('/api/channels', methods=['GET'])
def channels():
    """
    <url>/api/channels

    View that Returns the channel

    """
    data = DB.session.execute('SELECT * FROM channels;')
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    return Response(json.dumps([dict(r) for r in data]), mimetype='application/json')


@MAIN_BP.route('/channels', methods=['GET'])
def show_channels():
    """
    <url>/api/channels

    View that Returns the channel and displays them in a nice table

    """
    data = DB.session.execute('SELECT * FROM channels;')
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    channels = [dict(r) for r in data]
    return render_template('channels.html', channels=channels)

@MAIN_BP.route('/delete/channel/<id>', methods=['GET', 'POST'])
def delete_channel(id):
    """
    <url>/

    View that Renders the Homepage

    """
    form = delete_form()
    if form.validate_on_submit():
        query = DB.session.execute("DELETE FROM channels WHERE channel_id={}".format(id))
        flash('Delete Successful!', 'success')
        return redirect(url_for('main.show_channels'))
    return render_template('delete_channel.html', form=form)

@MAIN_BP.route('/edit/channel/<id>', methods=['GET', 'POST'])
def edit_channel(id):
    """
    <url>/edit/<id>

    View that edits a Channel

    """
    entry = DB.session.execute('SELECT * FROM channels WHERE channel_id={};'.format(id)).fetchone()
    form = channel_form(obj=entry)

    if form.validate_on_submit():
        name = form.name.data
        ip = form.ip.data
        lang = form.lang.data
        country_code = form.country_code.data
        timezone = form.timezone.data

        query = DB.session.execute("UPDATE channels SET name='{}', ip='{}', country_code='{}', lang='{}', timezone='{}' WHERE channel_id={}".format(name, ip, country_code, lang, timezone, id))
        flash('Edit Successful!', 'success')
        return redirect(url_for('main.show_channels'))

    return render_template('edit_channel.html', form=form)

@MAIN_BP.route('/add/channel', methods=['GET', 'POST'])
def add_channel():
    """
    <url>/add/channel

    View that adds a Channel

    """
    form = channel_form()

    if form.validate_on_submit():
        name = form.name.data
        ip = form.ip.data
        lang = form.lang.data
        country_code = form.country_code.data
        timezone = form.timezone.data

        query = DB.session.execute("INSERT INTO channels (name, ip, \
            country_code, lang, timezone, status) \
            VALUES ('{}', '{}','{}', '{}', '{}', 'down')" \
            .format(name, ip, 
                country_code, lang, timezone))

        flash('Channel Added Successfuly!', 'success')
        return redirect(url_for('main.show_channels'))

    return render_template('edit_channel.html', form=form)
