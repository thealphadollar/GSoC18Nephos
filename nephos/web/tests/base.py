import os
import unittest
from flask_testing import TestCase
import flask
from webServer import app

class BaseTestCase(TestCase):
	def create_app(self): 
		# executed prior to each test
		def setUp(self):
			app.config['TESTING'] = True
			app.config['WTF_CSRF_ENABLED'] = False
			app.config['DEBUG'] = False
			app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
				os.path.join(app.config['BASEDIR'], '../../databases/jobs.db')
			self.app = app.test_client()
			db.create_all()

		return app 
		# executed after each test
		def tearDown(self):
			db.drop_all()

if __name__ == "__main__":
	unittest.main()

