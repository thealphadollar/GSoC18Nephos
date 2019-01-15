"""
Used to Create a Base for testing the flask app
"""
import os
import unittest
from flask_testing import TestCase
from nephos.web.webServer import APP
from nephos.web.info_panel import create_app

class BaseTestCase(TestCase):
	# executed prior to each test
	def create_app(self):
		app = create_app()
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		pass

	def tearDown(self):
		pass
