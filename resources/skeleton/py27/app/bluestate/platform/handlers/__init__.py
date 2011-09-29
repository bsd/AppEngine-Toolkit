# -*- coding: utf-8 -*-
import os
import config
import hashlib
import logging
import werkzeug

try:
	import json as simplejson
except ImportError:
	import simplejson

# ProtoRPC Imports
from protorpc import remote

# Tipfy Imports
from tipfy import RequestHandler, Response
from tipfyext.jinja2 import Jinja2Mixin

from tipfy.i18n import I18nMiddleware
from tipfy.sessions import SessionMiddleware

# App Engine Imports
from google.appengine.ext import db
from google.appengine.api import xmpp
from google.appengine.api import mail
from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.api import channel
from google.appengine.api import backends
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.api import namespace_manager

# Handler Mixins
from bluestate.platform.core.output.live import LiveServices
from bluestate.platform.core.output.assets import AssetsMixin
from bluestate.platform.core.output.sessions import SessionsMixin


class BlueStateHandler(RequestHandler):

	''' Top-level handler for everything in BSD App Engine. '''

	### === Shortcuts to Tipfy & APIs === ###
	db = db
	mail = mail
	xmpp = xmpp
	channel = channel	
	memcache = memcache
	response = Response

	### === Base Values === ###
	baseHeaders = {
		
		# HTTP response headers
		'X-Platform': 'BlueState/AppTools-Embedded', # Indicate the platform that is serving this request
		'X-Powered-By': 'Google App Engine/1.5.2', # Indicate the SDK version
		'X-UA-Compatible': 'IE=edge,chrome=1' # Enable compatibility with Chrome Frame, and force IE to render with the latest engine

	}
	
	baseContext = {
	
		## Python functions
		'all': all, 'any': any,
		'int': int, 'str': str,
		'len': len, 'map': map,
		'max': max, 'min': min,
		'zip': zip, 'bool': bool,
		'list': list, 'dict': dict,
		'tuple': tuple, 'range': range,
		'round': round, 'slice': slice,
		'xrange': xrange, 'filter': filter,
		'reduce': reduce, 'sorted': sorted,
		'unicode': unicode,	'reversed': reversed,
		'isinstance': isinstance, 'issubclass': issubclass,
	
		## Utility stuff
		'util': {

			'environ': os.environ,		
			'config': {
				'get': config.config.get,
				'debug': config.debug
			},
		
		},
		
		## API Shortcuts
		'api': {
		
			'oauth': oauth,
			'users': {
				'is_current_user_admin': users.is_current_user_admin,
				'current_user': users.get_current_user,
				'create_login_url': users.create_login_url,
				'create_logout_url': users.create_logout_url
			},
			'backends': backends,
			'multitenancy': namespace_manager
		
		}
			
	}

	
	### === Config + Util Properties === ###
	@werkzeug.cached_property
	def _outputConfig(self):
		return config.config.get('project.output', {})

	@werkzeug.cached_property
	def _handlerConfig(self):
		return config.config.get('project.output.handler', {})



class WebHandler(BlueStateHandler, Jinja2Mixin, AssetsMixin, LiveServices, SessionsMixin):

	''' Top-level parent class for web request handlers based in Tipfy. '''
	
	#middleware = [SessionMiddleware(), I18nMiddleware()]
		
	
	### === Internal Methods === ###
	def _bindTemplateContext(self, params, output_cfg):

		''' Bind utility functions and variables to the template context. '''

		# Bind Tipfy & util functions
		params['link'] = self.url_for
		params['config'] = config.config.get
		params['environ'] = os.environ.get
		
		# System Config
		params['sys'] = {'config': {}}
		params['sys']['environ'] = os.environ
		params['sys']['config']['output'] = self._outputConfig		

		# Bind AssetMixin functions
		params['asset'] = {}
		params['asset']['img'] = self.assets.img_url
		params['asset']['style'] = self.assets.style_url	
		params['asset']['script'] = self.assets.script_url
		
		# Page Parameters
		params['page'] = {}
		params['page']['manifest'] = False
		params['page']['elements'] = {
			'errorNotice': False,
			'infoNotice': False,
			'generalNotice': False,
			'successNotice': False
		}
		try:
			params['page']['standalone'] = int(self.request.args.get('_s', 0)) or self._outputConfig.get('standalone', False)
		except Exception:
			params['page']['standalone'] = False
			
		# Appcaching
		if self._outputConfig.get('appcache', False) is not False:
			if self._outputConfig.get('appcache').get('enable', False) == True or self.request.args.get('_ac', False) == True:
					manifest = self._outputConfig.get('appcache').get('manifest', None)
					if manifest is not None:
						params['page']['manifest'] = manifest
		
		# Bind App Engine functions
		params['api'] = {
			'oauth': oauth,
			'users': {
				'is_user_admin': users.is_current_user_admin,
				'current_user': users.get_current_user,
				'create_login_url': users.create_login_url,				
				'create_logout_url': users.create_logout_url,
			},
			'backends': backends,
			'multitenancy': namespace_manager
		}
		
		# Bind Live Services (channel functions)
		params['live'] = {
			
			'get_lib': self.getChannelLib,
			'get_channel': self.getLiveChannel
			
		}
		

	### === Public Methods === ###
	def render(self, path, context={}, elements={}, content_type='text/html', headers={}, **kwargs):

		''' Return a response containing a rendered Jinja template. Create a session if one doesn't exist. '''
	
		self.context['user'] = users.get_current_user()
		self.context['session'] = self.getBSDSession()
		
		### Build HTTP response headers
		response_headers = {}
		for key, value in self.baseHeaders.items(): ## Base headers first
			response_headers[key] = value
		if len(headers) > 0: ## Render headers second
			for key, value in headers.items():
				response_headers[key] = value
		

		### Build template context
		if len(kwargs) > 0:
			for k, v in kwargs.items():
				self.context[k] = v ## Kwargs override context
		
		# Bind base vars
		self._bindTemplateContext(self.context, self._outputConfig)
		
		# Bind elements
		for element, config in elements.items():
			self.context['page']['elements'][element] = config
		
		
		#### Source transform
		source_transform = unicode # default to unicode

		if self._outputConfig.get('minify', False) is True: # minification
			try:
				import slimmer
				if content_type == 'text/html':
					source_transform = slimmer.html_slimmer
				elif content_type == 'text/javascript':
					from slimmer.js_function_slimmer import slim as slimjs
					source_transform = slimjs
				elif content_type == 'text/css':
					source_transform = slimmer.css_slimmer
			except ImportError, e:
				if not config.debug:
					source_transform = unicode
				else:
					raise
						
		return self.response(response=source_transform(self.render_template(path, **self.context)), content_type=content_type, headers=[(key, value) for key, value in response_headers.items()])