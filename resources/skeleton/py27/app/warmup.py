"""
Warmup request handler - imports and caches a bunch of data to prepare for requests. Always responds with a 200 OK.

"""

## Get ready
import os
import sys
import bootstrap

bootstrap.BlueStateBootstrapper.prepareImports()

## Libraries
import ndb
import webob
import tipfy
import jinja2
import config
import logging
import webapp2
import slimmer
import protorpc
import pipeline
import werkzeug
import mapreduce
import webapp2_extras
import wsgiref.handlers
import ProvidenceClarity

## GAE APIs
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import runtime
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.api import datastore
from google.appengine.api import taskqueue

## GAE Ext
from google.appengine.ext import db
from google.appengine.ext import gql
from google.appengine.ext import search
from google.appengine.ext import bulkload

## Blue State
import bluestate

def respond200():
	if config.debug:
		logging.debug('Warming up interpreter caches...')

	print "HTTP/1.1 200 OK"
	print "Content-Type: text/plain"
	print ""
	print "WARMUP_SUCCESS"

if __name__ == '__main__':
	respond200()