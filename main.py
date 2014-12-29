import webapp2
import logging
from google.appengine.ext import ndb


class Stops(ndb.Model):
    stop_id  = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    name = ndb.StringProperty(required = True)
    location = ndb.GeoPtProperty(required = True)

class Routes(ndb.Model):
    routes_id = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)

class Mapping(ndb.Model):
    stop_id = ndb.StringProperty(required = True)
    routes_id = ndb.StringProperty(required = True)

class MainHandler(webapp2.RequestHandler):
  pass

class FrontPage(MainHandler):
  ""
  def get(self):
    self.response.out.write('Hello World!')


app = webapp2.WSGIApplication([('/', FrontPage)])
