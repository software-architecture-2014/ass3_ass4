#-*- coding: UTF-8 -*-
import webapp2
import logging
import codecs
import jinja2
import os
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
    route_id = ndb.StringProperty(required = True)

class MainHandler(webapp2.RequestHandler):
  #init jinja
  def encode_list(self, l):
    return [ codecs.encode(word, 'utf-8') for word in l ]

  jinja_environment = jinja2.Environment(autoescape=True, 
      loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "dynamicHTML")))

class BrowsePage(MainHandler):
  ""
  def get(self):
    #self.response.out.write(url)
    stops = [ s.name for s in Stops.query().fetch() ]
    stops = sorted(list(set(stops)))
    p = self.jinja_environment.get_template("Browse.html").render(stops = stops)
    self.response.out.write(p)

class FilterPage(MainHandler):
  ""
  def get(self):
    p = self.jinja_environment.get_template("Filter.html").render()
    self.response.out.write(p)

class ConnectionPage(MainHandler):
  ""
  def get(self):
    p = self.jinja_environment.get_template("Connection.html").render()
    self.response.out.write(p)

class FilterResult(MainHandler):
  ""
  def get(self):
    name = self.request.get('Name')
    lat  = self.request.get('Lat')
    lon  = self.request.get('Lon')

    query_obj = Stops.query()
    if name:
      stops = [ s for s in query_obj.fetch() if s.name.lower().startswith(name.lower()) ]
    else:
      stops = query_obj.fetch()
    try:
      if lat:
        stops = [ s for s in stops if s.location.lat > float(lat) ]

      if lon:
        stops = [ s for s in stops if s.location.lon > float(lon) ]
    except ValueError:
      self.response.out.write("an error occurred! Try a valid Latitude/Longitude")
      return
      
    stops = [ s.name for s in stops ]
    stops = sorted(list(set(self.encode_list(stops))))
    self.response.out.write(stops)

class ConnectResult(MainHandler):
  ""
  def get(self):
    first_stop = self.request.get('First')
    sec_stop   = self.request.get('Sec')

    if first_stop and sec_stop:
      #First get the Stop IDs
      first_ids = Stops.query().filter(Stops.name == first_stop.capitalize()).fetch()
      sec_ids   = Stops.query().filter(Stops.name == sec_stop).fetch()
      
      #todo next: get all routes where those ids are in
      first_ids = [ s.stop_id for s in first_ids ]
      sec_ids   = [ s.stop_id for s in sec_ids ]

      routes_ids = Mapping.query(Mapping.stop_id.IN(first_ids)).fetch()
      self.response.out.write(first_ids)
class Erstelle(MainHandler):
#20911104    15.4526367    47.0593698    Moserhofgasse
  
  def get(self):
    ndb.delete_multi( Stops.query().fetch(keys_only=True) )
    ndb.delete_multi( Mapping.query().fetch(keys_only=True) )
    ndb.delete_multi( Routes.query().fetch(keys_only=True) )

    all_stops, all_mappings, all_routes = [], [], []

    with codecs.open('stops.csv', 'r', 'utf-8') as input_file:
      all_lines = input_file.readlines()

    for line in all_lines[1:]:
      words = line.split()
      stop = Stops(stop_id = words[0],
                   location = ndb.GeoPt(", ".join( words[1:3][::-1])),
                   name = " ".join(self.encode_list(words[3:])))
      all_stops.append(stop)

    with codecs.open('mapping.csv', 'r', 'utf-8') as input_file:
      all_lines = input_file.readlines()

    for line in all_lines[1:]:
      words = line.split('|')
      all_mappings.append(Mapping(stop_id = words[1],
                                  route_id = words[0]))

    with codecs.open('routes.csv', 'r', 'utf-8') as input_file:
      all_lines = input_file.readlines()

    for line in all_lines[1:]:
      words = line.split('|')
      all_routes.append(Routes(routes_id = words[0],
                               name = words[1]))

    ndb.put_multi(all_stops)
    ndb.put_multi(all_mappings)
    ndb.put_multi(all_routes)

    self.response.out.write('All done')

app = webapp2.WSGIApplication([('/app/Browse.html', BrowsePage),
                               ('/app/Filter.html', FilterPage),
                               ('/app/Connection.html', ConnectionPage),
                               ('/app/filteredStation', FilterResult),
                               ('/app/ConnStation',ConnectResult)])
