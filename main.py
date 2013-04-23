import webapp2
import jinja2
import re
import hashlib

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images
from models import Passenger, Driver, Passenger_Request, Connected, Driver_Request

template_dir = "templates"
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

def make_id_hash(id):
    honey = 'to.be.or.not.to.be'
    id_hash = str(id) + honey
    return hashlib.sha256(id_hash).hexdigest() + '|' + str(id)


def check_id_hash(id):
    honey = 'to.be.or.not.to.be'
    id_hash = str(id) + honey
    return hashlib.sha256(id_hash).hexdigest() + '|' + str(id)


def delete_cookie(self, name):
    set_cookie(self, name, "-")


def set_cookie(self, name, value):
    self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, value))


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
#        self.redirect('/signup?state=%s')
        self.redirect('/signup')

class SignupHandler(Handler):
    def get(self):
<<<<<<< HEAD
        self.render("google.html")
        
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
            
class DriverHome(Handler):
    def get(self):
        passenger_requests = Passenger_Request.gql("ORDER BY created")
        self.render("driver_home.html", passenger_requests = passenger_requests)
        
class ImageHandler(Handler):
    def get(self):
        passenger = db.get(self.request.get('img_key'))
        if passenger.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.write(passenger.picture)
=======
#        if state == 'logout':
#            delete_cookie(self, 'id')
#        else:
#            currentUser = self.request.cookies.get("id")
#            if currentUser:
#                list = currentUser.split('|')
#                checkUser = check_id_hash(list[1])
#                if currentUser == checkUser:
#                    self.redirect("/%d" % (int(list[1])))
        self.render("new.html", error="")

    def post(self):
        action = self.request.get("action")
        if action == "Login":
            phone_number = self.request.get("phone_number")
            password = self.request.get("password")
            status, user = Passenger.check_passenger(phone_number, password)
            if status:
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                self.redirect('/passenger')
            else:
                error ='Invalid login details'
                self.render("new.html", error=error)

        elif action == "Create Account":
            email = self.request.get("email")
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            phone_number = self.request.get("new_phone_number")
            password = self.request.get("new_password")
#            user_type = self.request.get("userOption")
            status, user = Passenger.create_passenger(email, first_name,last_name, phone_number, password)
            if status:
                error = 'Phone number is already in use.'
                self.render("new.html", error=error)
            else:
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                self.redirect("/passenger")
#                % (int(user.key().id()))

class PassengerHandler(Handler):
    def get(self):
        self.render("passenger.html")

#    def post(self):
#        phone_number = self.request.cookies.get("number")
#        passenger = Passenger.gql("WHERE phone_number = :1", phone_number)
#        current_location = self.request.get("current_location")
#        destination = self.request.get("destination")
#        price_offer = self.request.get("price")
#        info = self.request.get("other_info")
#
#        if current_location:
#            current_split = current_location.split(" ")
#
#        if passenger and current_location and destination and price_offer:
#            request = Passenger_Request(passenger = passenger, current_location = current_location, destination = destination, price_offer = price_offer, other_info = info)
#            request.put()
#
#class DriverHandler(Handler):
#    def get(self):
#        self.render("driver.html")
#
#    def post(self):
#        phone_number = self.request.cookies.get("number")
#        driver = Driver.gql("WHERE phone_number = :1", phone_number)
#        current_location = self.request.get("current_location")
#        destination = self.request.get("destination")
#
#        if driver and current_location and destination:
#            request = Driver_Request(driver = driver, current_location = current_location, destination = destination)
#            request.put()
#        else:
#            self.write("Fill it all out")
>>>>>>> 1bfba0deb496dddf37c76da27349e72e7db914c3

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/logout', SignupHandler),
    ('/signup', SignupHandler),
<<<<<<< HEAD
    ('/passenger', PassengerHandler),
    ('/driver', DriverHandler),
    ('/home', DriverHome),
    ('/img', ImageHandler)
    
    
=======
    ('/passenger' , PassengerHandler),
#    ('/driver', DriverHandler)
>>>>>>> 1bfba0deb496dddf37c76da27349e72e7db914c3
], debug=True)
