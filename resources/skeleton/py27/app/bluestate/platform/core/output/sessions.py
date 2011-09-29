from bluestate.platform.core.api.output import HandlerMixin
from bluestate.platform.core.api.sessions import CoreSessionsAPI


class SessionsMixin(HandlerMixin):
	
	_sessions_api = CoreSessionsAPI()
	
	def getBSDSession(self):
		
		if 'client' not in self.session or 'sid' not in self.session:
			if 'client' not in self.session:
				self.session['client'], self.session['sid'] = self._sessions_api.keyFactory()
			else:
				self.session['sid'] = self._sessions_api.keyFactory(self.session['client'])
				
		else:
			return self.session