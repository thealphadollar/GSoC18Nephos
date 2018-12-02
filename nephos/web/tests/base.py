import os
import unittest
from flask_testing import TestCase
import flask
from webServer import APP


class BaseTestCase(TestCase):
    def create_app(self):
        # executed prior to each test
        def setUp(self):
            APP.config['TESTING'] = True
            APP.config['WTF_CSRF_ENABLED'] = False
            APP.config['DEBUG'] = False
            APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                os.path.join(APP.config['BASEDIR'], '../../databases/jobs.db')
            self.APP = APP.test_client()
            db.create_all()

        return APP
        # executed after each test

        def tearDown(self):
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
