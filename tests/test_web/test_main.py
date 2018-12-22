"""
Test Controller responsible for testing all the views in the /main folder
"""
from unittest import TestCase, mock
from tests.test_web.base import BaseTestCase
from nephos.web.info_panel import APP, DB

jobs_engine = DB.get_engine(APP, 'jobs')

class test_Controllers(BaseTestCase):
    """
    Test Cases for the Main Views
    """

    def test_root(self):
        """
        Test the root
        """
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello World!')

    def test_channels_view(self):
        """
        Test if Channel works properly
        """
        response = self.app.test_client().get('/channels')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('channels.html')

    def test_jobs_api(self):
        """
        Test if Jobs API works properly
        """
        response = self.app.test_client().get('/api/channels')
        self.assertEqual(response.status_code, 200)
        self.assertIn("bloomberg_europe", str(response.data))
        self.assertIn("EU", str(response.data))
        self.assertIn("239.255.20.19:1234", str(response.data))
        self.assertIn("spa", str(response.data))
        self.assertIn("up", str(response.data))

    def test_jobs(self):
        """
        Test if Jobs works properly
        """
        response = self.app.test_client().get('/jobs')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('jobs.html')

    def test_channel_add(self):
        """
        Test Adding Channels
        """
        data = dict(name="kanal5", ip="31.12.16.0", country_code="mkd", lang="mkd", timezone="utc",
                    submit=True)
        response = self.app.test_client().get(
            '/add/channel', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        #self.assertMessageFlashed('Channel Added Successfuly!')
        self.assertIn('Channel Added Successfuly!', str(response.data))

        query = DB.session.execute(
            'SELECT * FROM channels WHERE name="kanal5').firstone()
        self.assertEqual(query['name'], 'kanal5')

    def test_channel_edit(self):
        """
        Test Edit for Channel
        """

        # Create New Channel
        data = dict(name="kanal5", ip="31.12.16.0",
                    country_code="mkd", lang="mkd", timezone="utc")

        response = self.app.test_client().post(
            '/add/channel', data=data, follow_redirects=True)

        # Get ID of what we want to edit
        query_to_change = DB.session.execute(
            'SELECT * FROM channels WHERE name="kanal5"').fetchone()

        # Edit Channel
        data = dict(name="1tv", ip="31.12.16.0", country_code="mkd", lang="mkd", timezone="utc",
                    submit=True)

        response = self.app.test_client().get('/edit/channel/{}'
            .format(query_to_change['channel_id']),
                                              data=data, follow_redirects=True)
        print(str(query_to_change['channel_id']))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Successful!', str(response.data))

    def test_channel_delete(self):
        """
        Test Delete for Channel
        """
        # Create New Channel
        data = dict(name="kanal5", ip="31.12.16.0",
                    country_code="mkd", lang="mkd", timezone="utc")

        response = self.app.test_client().post(
            '/add/channel', data=data, follow_redirects=True)

        # Get ID of what we want to edit
        query_to_change = DB.session.execute(
            'SELECT * FROM channels WHERE name="kanal5"').fetchone()

        response = self.app.test_client().get('/delete/channel/{}'
                                            .format(query_to_change['channel_id']), 
                                              data=dict(submit=True), 
                                              follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Delete Successful!', str(response.data))

    def test_job_add(self):
        """
        Test Addition for Jobs
        """

        data = dict(name="Love", channel_name="RandomTV",
                    start_time="15:51", duration=60, rep="1010000", submit=True)

        response = self.app.test_client().post(
            '/add/job', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Job Added Successfuly!', str(response.data))

    def test_job_edit(self):
        """
        Test Editting for Jobs
        """

        data = dict(name="Rick And Morty", channel_name="RandomTV",
                    start_time="15:51", duration=60, rep="1010000", submit=True)

        response = self.app.test_client().post(
            '/edit/job/RandomTV', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Successful!', str(response.data))

    def test_job_deletion(self):
        """
        Test Addition for Jobs
        """
        data_raw = jobs_engine.execute('SELECT * FROM apscheduler_jobs;').fetchone()
        name = data_raw['next_run_time']

        response = self.app.test_client().post(
            '/delete/job/{}'.format(name), data=dict(Submit=True), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Delete Successful!', str(response.data))
        