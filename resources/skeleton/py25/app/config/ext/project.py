""" 

	######################################## BSD Project configuration. ########################################

"""
config = {}


## App settings
config['bluestate.project'] = {

	'version': {
		'major': 1,
		'minor': 0,
		'micro': 0,
		'build': 20110915,
		'release': 'ALPHA'
	}

}

## Development/debug settings
config['bluestate.project.dev'] = {

}

## Output layer settings
config['bluestate.project.output'] = { 

	'minify': False,
	'watermark': True,
	'standalone': False,

	'appcache': {
		'enable': False,
		'manifest': '<relative path to manifest>'
	},

	'assets':{
		'minified': False,
		'serving_mode': 'local', ## 'local' or 'cdn' (CDN prefixes all assets with an absolute URL)
		'cdn_prefix': '<hostname for cdn, or list of cdn hostnames>'
	}

}

## Caching
config['bluestate.project.cache'] = {

	'key_seperator': '::',
	'prefix': 'dev',
	'prefix_mode': 'explicit',
	'prefix_namespace': False,
	'namespace_seperator': '::',
	
	'adapters': {

		'fastcache': {

			'default_ttl': 600
	
		},
		
		'memcache': {

			'default_ttl': 10800
		
		}, 
		
		'backend': {

			'default_ttl': 10800

		},

		'datastore': {

			'default_ttl': 86400
		
		}
			
	}

}

config['bluestate.project.output.template_loader'] = {

	'force': True, ## Force enable template loader even on Dev server
	'debug': False,  ## Enable dev logging
	'use_memory_cache': False, ## Use handler in-memory cache for template source
	'use_memcache': False, ## Use Memcache API for template source

}

# BSD Pipelines Configuration
config['bluestate.project.pipelines'] = {

    'debug': False, # Enable basic serverlogs
	'logging': {
	
		'enable': True, # Enable the pipeline logging subsystem
		'mode': 'serverlogs', # 'serverlogs', 'xmpp' or 'channel'
		'channel': '', # Default channel to send to (admin channels are their email addresses, this can be overridden on a per-pipeline basis in the dev console)
		'jid': '', # Default XMPP JID to send to (this can be overridden on a per-pipeline basis in the dev console)
	
	}

}