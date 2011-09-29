# -*- coding: utf-8 -*-
"""URL definitions."""

from tipfy.routing import Rule
from tipfy.routing import HandlerPrefix

rules = [

	HandlerPrefix('bluestate.project.handlers.', [
	
	    Rule('/', name='landing', handler='main.Landing'),
	
	])

]