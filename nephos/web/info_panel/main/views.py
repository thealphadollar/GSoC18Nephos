"""
main/views.py

Controller Responsible for Handling the main page

"""

# Sigh, I didn't thought it would end up this far just to import the recorder
import sys
sys.path.append("../..")

from logging import getLogger
import json
from datetime import datetime
from flask import render_template, Response, redirect, url_for, flash
from nephos.recorder.jobs import JobHandler
from nephos.recorder.channels import ChannelHandler
from nephos.manage_db import DBHandler
from nephos.exceptions import DBException
from nephos.scheduler import Scheduler
from nephos import validate_entries
from ..main import MAIN_BP
from ..main.forms import DeleteForm, ChannelForm, JobForm
from .. import DB, APP


LOG = getLogger(__name__)

# We need to Pass a Scheduler Object and initialize the Class so we can insert the jobs
scheduler = Scheduler(True)
JOBS_SCHEDULER = JobHandler(scheduler)
CHANNEL_HANDLER = ChannelHandler()

JOBS_ENGINE = DB.get_engine(APP, 'jobs')



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
    data = CHANNEL_HANDLER.grab_ch_list()
    return Response(json.dumps(data), mimetype='application/json')


@MAIN_BP.route('/channels', methods=['GET'])
def show_channels():
    """
    <url>/channels

    View that Returns the channel and displays them in a nice table

    """
    data = CHANNEL_HANDLER.grab_ch_list()
    return render_template('channels.html', channels=data)


@MAIN_BP.route('/api/jobs', methods=['GET'])
def jobs():
    """
    <url>/api/jobs

    View that Returns the jobs

    """

    # This is Used to get the Jobs Database instead of storage.db
    data_raw = JOBS_ENGINE.execute('SELECT * FROM apscheduler_jobs;')

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
    data_raw = JOBS_ENGINE.execute('SELECT * FROM apscheduler_jobs;')

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

        payload = {
            0: {
                "name": name,
                "ip": ip,
                "country_code": country_code,
                "lang": lang,
                "timezone": timezone
            }
        }

        CHANNEL_HANDLER.insert_channels(payload)

        # Insert The Data from the Form into the Database

        flash('Channel Added Successfuly!', 'success')
        return redirect(url_for('main.show_channels'))

    # Instead of Creating an Add template for the same form, i've reused this one
    return render_template('edit_channel.html', form=form)


@MAIN_BP.route('/delete/job/<name>', methods=['GET', 'POST'])
def delete_job(name):
    """
    <url>/delete/job/<name>

    View that Deletes a Job

    """
    # Select The Form
    form = DeleteForm()

    # Validate if Form Statisfies Everything
    if form.validate_on_submit():
        # Execute Deletion but Select the other Database
        data = {
            0: {
                'name': name
            }
        }
        JOBS_SCHEDULER.rm_jobs(job_data=data)
        flash('Delete Successful!', 'success')
        return redirect(url_for('main.show_jobs'))
    return render_template('delete_job.html', form=form)

# There is no Function to Update the jobs
@MAIN_BP.route('/edit/job/<name>', methods=['GET', 'POST'])
def edit_job(name):
    """
    <url>/edit/job/<name>

    View that edits a Job
    """
    

    # Select The Other Database and Find The Record
    form = JobForm()

    # Validate That Everything is statisfied in the Form
    if form.validate_on_submit():

        # Delete The Previous One

        data = {
            0: {
                'name': name
            }
        }
        JOBS_SCHEDULER.rm_jobs(job_data=data)

        # Add the Data and Clean Up the Data and Send only the needed stuff
        data = form.data
        if 'csrf_token' in data:
            data.pop('csrf_token')
        data.pop('submit')
        print(data)

        try:
            # insert_jobs needs a DB connection so why not open another one
            with DBHandler.connect() as db_cur:
                #  Insert the data and redirect
                JOBS_SCHEDULER.insert_jobs(db_cur, data)
                flash('Edit Successful!', 'success')
                return redirect(url_for('main.show_jobs'))
        except DBException as err:
            # Well something went wrong might as well log it and alert
            flash('Editting failed!', 'danger')
            LOG.warning("Data addition failed")
            LOG.debug(err)
            return redirect(url_for('main.show_jobs'))


    return render_template('edit_job.html', form=form)


@MAIN_BP.route('/add/job', methods=['GET', 'POST'])
def add_job():
    """
    <url>/add/job

    View that adds a Job

    """
    # Select the Form
    form = JobForm()

    if form.validate_on_submit():
        # Clean Up Data and Send only the needed stuff
        data = form.data
        if 'csrf_token' in data:
            data.pop('csrf_token')
        data.pop('submit')

        # This is the payload
        payload = {
            0:{}
        }

        payload[0] = data

        print(payload)

        try:
            # insert_jobs needs a DB connection so why not open another one
            with DBHandler.connect() as db_cur:
                #  Insert the data and redirect
                JOBS_SCHEDULER.insert_jobs(db_cur=db_cur, job_data=validate_entries(payload))
                flash('Job Added Successfuly!', 'success')
                return redirect(url_for('main.show_jobs'))
        except DBException as err:
            # Well something went wrong might as well log it and alert
            flash('Job Addition failed!', 'danger')
            LOG.warning("Data addition failed")
            LOG.debug(err)
            return redirect(url_for('main.show_jobs'))

    return render_template('edit_job.html', form=form)
