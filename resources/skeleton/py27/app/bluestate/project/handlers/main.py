import os
import sys
import config

from google.appengine.api import backends
from google.appengine.api import app_identity

from bluestate.platform.handlers import WebHandler


class Landing(WebHandler):
	
	def get(self):
		return self.render('main/landing.html', title='Welcome - BSD App Tools', version=sys.version, sysconfig=config.config.get('bluestate.project'), appid=app_identity.get_application_id(), instanceid=backends.get_instance())