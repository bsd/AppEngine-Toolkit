from bluestate.platform.core.exceptions import BSDCoreException


class CoreOutputAPIException(BSDCoreException):
	pass
	
## == Assets Module Exceptions == ##
class AssetException(CoreOutputAPIException): pass
class InvalidAssetType(AssetException): pass
class InvalidAssetEntry(AssetException): pass


class HandlerMixin(object):
	pass