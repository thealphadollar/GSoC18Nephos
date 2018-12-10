"""
main/views.py

Controller Responsible for Handling the main page

"""
import json
from datetime import datetime
from flask import render_template, Response, redirect, url_for, flash
from ..main import MAIN_BP
from ..main.forms import DeleteForm, ChannelForm, JobForm
from .. import DB, APP


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
    <url>/channels

    View that Returns the channel and displays them in a nice table

    """
    data = DB.session.execute('SELECT * FROM channels;')
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    channels = [dict(r) for r in data]
    return render_template('channels.html', channels=channels)


@MAIN_BP.route('/api/jobs', methods=['GET'])
def jobs():
    """
    <url>/api/jobs

    View that Returns the jobs

    """

    # This is Used to get the Jobs Database instead of storage.db
    jobs_engine = DB.get_engine(APP, 'jobs')
    data_raw = jobs_engine.execute('SELECT * FROM apscheduler_jobs;')

    data = {}

    number = 0

    # Put Everything in a Global Dict so we can later send it as a JSON
    for row in data_raw:
        # This Function exists because the one line solution didn't work

        # Create a Dictionary and Put it inside a Main Dictionary
        dat = {'job_name': row[0], 'next_run_time': str(
            row[1]), 'job_state': str(row[2])}
        data[number] = dict(dat)
        number += 1

    return Response(json.dumps(data), mimetype='application/json')


@MAIN_BP.route('/jobs', methods=['GET'])
def show_jobs():
    """
    <url>/jobs

    View that Returns the jobs and displays them in a nice table
    """

    # This is Used to get the Jobs Database instead of storage.db
    jobs_engine = DB.get_engine(APP, 'jobs')
    data_raw = jobs_engine.execute('SELECT * FROM apscheduler_jobs;')

    data = {}

    number = 0

    # Convert into Dict so Jinja Can Easily Parse it
    for row in data_raw:
        # This Function exists because the one line solution didn't work

        # Convert to Human Readable Date
        timestamp = int(row[1])
        date = datetime.utcfromtimestamp(
            timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Create a Dictionary and Put it inside a Main Dictionary
        dat = {'channel_name': row[0], 'next_run_time': str(date)}
        data[number] = dict(dat)
        number += 1

    return render_template('jobs.html', jobs=data)


@MAIN_BP.route('/delete/channel/<id>', methods=['GET', 'POST'])
def delete_channel(id):
    """
    <url>/delete/channel/<id>

    View that Deletes a channel

    """
    # Set up the Form

    form = DeleteForm()
    # Validate if the Form statisfies everything in this case a button press
    if form.validate_on_submit():
        # Execute Deletion inside the database
        query = DB.session.execute(
            "DELETE FROM channels WHERE channel_id={}".format(id))
        flash('Delete Successful!', 'success')
        return redirect(url_for('main.show_channels'))
    return render_template('delete_channel.html', form=form)


@MAIN_BP.route('/edit/channel/<id>', methods=['GET', 'POST'])
def edit_channel(id):
    """
    <url>/edit/<id>

    View that edits a Channel

    """
    entry = DB.session.execute(
        'SELECT * FROM channels WHERE channel_id={};'.format(id)).fetchone()
    # Prefill Form with data from Database
    form = ChannelForm(obj=entry)

    # Validate if the Form statisfies everything
    if form.validate_on_submit():
        # Get The Data from the Form
        name = form.name.data
        ip = form.ip.data
        lang = form.lang.data
        country_code = form.country_code.data
        timezone = form.timezone.data

        # Update the Database Record
        query = DB.session.execute("UPDATE channels SET name='{}', ip='{}', \
            country_code='{}', lang='{}', timezone='{}' WHERE channel_id={}".format(
            name, ip, country_code, lang, timezone, id))
        flash('Edit Successful!', 'success')
        return redirect(url_for('main.show_channels'))

    return render_template('edit_channel.html', form=form)


@MAIN_BP.route('/add/channel', methods=['GET', 'POST'])
def add_channel():
    """
    <url>/add/channel

    View that adds a Channel

    """
    # Select The Form
    form = ChannelForm()

    # Validate if the Form statisfies everything
    if form.validate_on_submit():
        # Get the Data from the Form
        name = form.name.data
        ip = form.ip.data
        lang = form.lang.data
        country_code = form.country_code.data
        timezone = form.timezone.data

        # Insert The Data from the Form into the Database
        query = DB.session.execute("INSERT INTO channels (name, ip, \
            country_code, lang, timezone, status) \
            VALUES ('{}', '{}','{}', '{}', '{}', 'down')"
                                   .format(name, ip,
                                           country_code, lang, timezone))

        flash('Channel Added Successfuly!', 'success')
        return redirect(url_for('main.show_channels'))

    # Instead of Creating an Add template for the same form, i've reused this one
    return render_template('edit_channel.html', form=form)


# ========== Todo: Fix up Database Handlers here ↓

@MAIN_BP.route('/delete/job/<id>', methods=['GET', 'POST'])
def delete_job(id):
    """
    <url>/delete/job/<id>

    View that Renders the Homepage

    """

    # Select The Form
    form = DeleteForm()

    # Validate if Form Statisfies Everything
    if form.validate_on_submit():
        # Execute Deletion but Select the other Database
        jobs_engine = DB.get_engine(APP, 'jobs')
        query = jobs_engine.execute(
            "DELETE FROM apscheduler_jobs WHERE channel_id={}".format(id))
        flash('Delete Successful!', 'success')
        return redirect(url_for('main.show_jobs'))
    return render_template('delete_jobs.html', form=form)


@MAIN_BP.route('/edit/job/<id>', methods=['GET', 'POST'])
def edit_job(id):
    """
    <url>/edit/job/<id>

    View that edits a Job

    """

    # Select The Other Database and Find The Record
    jobs_engine = DB.get_engine(APP, 'jobs')
    #entry = jobs_engine.execute('SELECT * FROM apscheduler_jobs WHERE id={};'.format(id)).fetchone()
    entry = jobs_engine.execute(
        'SELECT * FROM apscheduler_jobs WHERE next_run_time=telediario_matinal;'
        .format(id)).fetchone()
    print(entry)
    form = JobForm(obj=entry)

    # Validate That Everything is statisfied in the Form
    if form.validate_on_submit():
        print(form.data)
        #query = DB.session.execute("UPDATE apscheduler_jobs SET next_run_time='{}' \
        #WHERE id={}".format(name, ip, country_code, lang, timezone, id))
        flash('Edit Successful!', 'success')
        return redirect(url_for('main.show_jobs'))

    return render_template('edit_job.html', form=form)


@MAIN_BP.route('/add/job', methods=['GET', 'POST'])
def add_job():
    """
    <url>/add/job

    View that adds a Job

    """
    form = JobForm()

    if form.validate_on_submit():
        DB.session.execute("INSERT INTO apscheduler_jobs (name, ip, \
            country_code, lang, timezone, status) \
            VALUES ('{}', '{}','{}', '{}', '{}', 'down')"
                                   .format(name, ip,
                                           country_code, lang, timezone))

        flash('Job Added Successfuly!', 'success')
        return redirect(url_for('main.show_jobs'))

    return render_template('edit_job.html', form=form)
