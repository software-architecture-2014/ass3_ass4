import webapp2
import logging
from google.appengine.ext import ndb



class MainHandler(webapp2.RequestHandler):
  pass

class FrontPage(MainHandler):
  ""
  def get(self):
    self.response.out.write('Hello World!')


app = webapp2.WSGIApplication([('/', FrontPage)])