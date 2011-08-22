import os
from bluestate.platform.handlers import WebHandler


class HelloWorldHandler(WebHandler):
	
	def get(self):
		return self.response('<b>sup</b>')
		
		
class PrettyHelloWorldHandler(WebHandler):
	
	def get(self):
		return self.render('main/landing.html', ip=os.environ['REMOTE_ADDR'])