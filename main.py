#-*- coding: UTF-8 -*-
import webapp2
import logging
import codecs
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

class Erstelle(MainHandler):
#20911104    15.4526367    47.0593698    Moserhofgasse
  
  def encode_list(self, l):
    return [ codecs.encode(word, 'utf-8') for word in l ]

  def get(self):
    ndb.delete_multi( Stops.query().fetch(keys_only=True) )
    all_stops = []

    with codecs.open('stops.csv', 'r', 'utf-8') as input_file:
      all_lines = input_file.readlines()
      for line in all_lines[1:]:

        words = line.split()
        stop = Stops(stop_id = words[0],
                     location = ndb.GeoPt(", ".join( words[1:3][::-1])),
                     name = " ".join(self.encode_list(words[3:])))

        all_stops.append(stop)

    ndb.put_multi(all_stops)

app = webapp2.WSGIApplication([('/', FrontPage),
                               ('/erstelle', Erstelle)])
