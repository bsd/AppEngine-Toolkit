# -*- coding: utf-8 -*-
import os
import sys
import logging
import datetime
import bootstrap

if 'lib' not in sys.path or 'lib/distlib' not in sys.path:
	bootstrap.BlueStateBootstrapper.prepareImports()

_config = {}
_compiled_config = None

## Check if we're running the app server
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


""" 

	######################################## Tipfy configuration. ########################################

"""
_config['tipfy'] = {

	# Basic Config Values
	#'server_name': 'localhost:8080' if debug == True else 'spi.wirestone.staging.ext.providenceclarity.com',

	# Installed middleware modules
	'middleware': [

	    # Display Midleware
	    #'tipfy.ext.i18n.I18nMiddleware',  ## Enables automatic string translations based on locale of user

	    # Debugging Middleware
	    'tipfy.ext.debugger.DebuggerMiddleware',  ## Enable debugger. It will be loaded only when executed from the dev environment.
	    'tipfy.ext.appstats.AppstatsMiddleware',  ## Enable for good code profiling information
    
	],

	'apps_installed':[
		'bluestate.platform', ## Platform files
		'bluestate.project' ## Site files
	],

}
_config['tipfy.sessions'] = {

	'secret_key':'DIOVOUBRUVB$(&&@#(#@&G(CVC(V@))))',
    'default_backend': 'datastore',
    'cookie_name':     'bsdappsession',
    'session_max_age': None,
    'cookie_args': {
        'max_age':     86400,
        #'domain':      '*',
        'path':        '/',
        'secure':      False,
        'httponly':    False,
    }	

}
_config['tipfyext.jinja2'] = {

	'templates_dir': 'templates/source', ## Root directory for template storage
	'templates_compiled_target': 'templates/compiled', ##  Compiled templates directory
	'force_use_compiled': False, ## Force Jinja to use compiled templates, even on the Dev server

	'environment_args': { ## Jinja constructor arguments
		'optimized': True,	## 
	    'autoescape': True, ## Global Autoescape. BE CAREFUL WITH THIS.
	    'extensions': ['jinja2.ext.autoescape', 'jinja2.ext.with_'],
	},

	'after_environment_created': 'bluestate.platform.core.output.factory.fcmOutputEnvironmentFactory', ## Map to the core output factory

}


""" 

	######################################## Core configuration. ########################################

"""
## System Config
_config['bluestate.system'] = {

	'debug': True, # System-level debug messages

	'hooks': { # System-level Developer's Hooks
		'appstats': {'enabled': False}, # AppStats RPC optimization + analysis tool
		'apptrace': {'enabled': False}, # AppTrace memory usage optimization + analysis tool
		'profiler': {'enabled': False}  # Python profiler for CPU cycle/efficiency optimization + analysis
	},
	
	'include': [ # Extended configuration files to include
		('platform', 'config.ext.platform'), # FCM/Momentum Platform config
		('fatcatmap', 'config.ext.project'), # FCM Site (Tipfy-layer) config
		('services', 'config.ext.services'), # Global + site services (RPC/API) config
		('assets', 'config.ext.assets') # Asset manangement layer config
	]

}

def systemLog(message, _type='debug'):
	global debug
	global _config
	prefix = '[CORE_SYSTEM]: '
	if _config['bluestate.system']['debug'] is True or _type in ('error', 'critical'):
		if _type == 'debug' or debug is True:
			logging.debug(prefix+message)
		elif _type == 'info':
			logging.info(prefix+message)
		elif _type == 'error':
			logging.error(prefix+message)
		elif _type == 'critical':
			logging.critical(prefix+message)


def readConfig(config=_config):
	global _compiled_config
	from werkzeug import import_string	
	if _compiled_config is not None:
		return _compiled_config
	else:
		if config['bluestate.system'].get('include', False) is not False and len(config['bluestate.system']['include']) > 0:
			systemLog('Considering system config includes...')
			for name, configpath in config['bluestate.system']['include']:
				systemLog('Checking include "'+str(name)+'" at path "'+str(configpath)+'".')
				try:
					for key, cfg in import_string('.'.join(configpath.split('.')+['config'])).items():
						config[key] = cfg
				except Exception, e:
					systemLog('Encountered exception of type "'+str(e.__class__)+'" when trying to parse config include "'+str(name)+'" at path "'+str(configpath))
					if debug:
						raise
					else:
						continue
		if len(config) > 0 and _compiled_config is None:
			_compiled_config = config
				
		return config
	
config = readConfig(_config)