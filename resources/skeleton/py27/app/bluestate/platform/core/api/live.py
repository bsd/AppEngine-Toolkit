from google.appengine.api import channel
from bluestate.platform.core.api import BlueStateCoreAPI
from bluestate.platform.core.api.cache import CoreCacheAPI


class CoreLiveAPI(BlueStateCoreAPI):


	def retrieveOrMakeChannelToken(self, seed):
		pass