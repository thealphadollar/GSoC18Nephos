"""
This are all the forms used in the Web app
"""
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, IntegerField


class ChannelForm(FlaskForm):
    """
    This Is a Form used to create new channels and edit existing ones
    """
    name = StringField('Channel Name', [validators.Length(min=2, max=50)])
    ip = StringField('IP Address')
    country_code = StringField(
        'Country Code', [validators.Length(min=3, max=5,)])
    lang = StringField('Language Code', [validators.Length(min=3, max=25)])
    timezone = StringField('Timezone', [validators.Length(min=3, max=5)])
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    """
    This is a Form that confirms Deletions
    """
    submit = SubmitField('Confirm')


class JobForm(FlaskForm):
    """
    This is a Form used to created new jobs and edit existing ones
    """
    name = StringField('Job Name', [validators.Length(min=2, max=50)])
    channel_name = StringField('Channel Name', [validators.Length(min=2, max=50)])
    start_time = StringField('Start Time [HH:MM]', [validators.Length(min=2, max=50)])
    duration = IntegerField('Duration in Minutes', [])
    rep = StringField('Run on [eg. 1010000 for monday and wednesday]', 
        [validators.Length(min=2, max=50)])
    submit = SubmitField('Submit')
