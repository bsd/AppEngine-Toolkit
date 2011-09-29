from bluestate.platform.core.api.live import CoreLiveAPI
from bluestate.platform.core.api.output import HandlerMixin


class LiveServices(HandlerMixin):

	__live_api = CoreLiveAPI()
		
		
	def getChannelLib(self):
		return '<script type="text/javascript" src="/_ah/channel/jsapi"></script>'
		
	def getLiveChannel(self, client):
		return self.__live_api.retrieveOrMakeChannelToken(client)