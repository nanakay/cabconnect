#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import re

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images
from models import Passenger, Driver, Passenger_Request, Connected, Driver_Request

template_dir = "templates"
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    """
    Parent class for all other webpages.
    """    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.redirect("/signup")
        
class SignupHandler(Handler):
    def get(self):
        self.render("home.html")
        
class PassengerHandler(Handler):
    def get(self):
        self.render("passenger.html")
        
    def post(self):
        phone_number = self.request.cookies.get("number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number)
        current_location = self.request.get("current_location")
        destination = self.request.get("destination")
        price_offer = self.request.get("price")
        info = self.request.get("other_info")
        
        if current_location:
            current_split = current_location.split(" ")
        
        if passenger and current_location and destination and price_offer:
            request = Passenger_Request(passenger = passenger, current_location = current_location, destination = destination, price_offer = price_offer, other_info = info)
            request.put()

class DriverHandler(Handler):
    def get(self):
        self.render("driver.html")
        
    def post(self):
        phone_number = self.request.cookies.get("number")
        driver = Driver.gql("WHERE phone_number = :1", phone_number)
        current_location = self.request.get("current_location")
        destination = self.request.get("destination")
        
        if driver and current_location and destination:
            request = Driver_Request(driver = driver, current_location = current_location, destination = destination)
            request.put()
        else:
            self.write("Fill it all out")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignupHandler),
    ('/passenger', PassengerHandler),
    ('/driver', DriverHandler)
    
    
], debug=True)
