import protorpc
from protorpc import remote

from bluestate.services.flags import audit
from bluestate.services.flags import caching
from bluestate.services.flags import security

from ProvidenceClarity.struct.util import DictProxy

from bluestate.services.core.service import BlueStateService


## Expose service flags (middleware decorators)
flags = DictProxy({

	'audit': DictProxy({
		'monitor': audit.Monitor,
		'debug': audit.Debug,
		'loglevel': audit.LogLevel,
	}),
	
	'caching': DictProxy({
		'local': caching.LocalCacheable,
		'memcache': caching.MemCacheable,
		'cacheable': caching.Cacheable,
	}),
	
	'security': DictProxy({
		'authorize': security.Authorize,
		'authenticate': security.Authenticate,
		'admin': security.AdminOnly
	})

})