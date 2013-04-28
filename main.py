import webapp2
import jinja2
import re
import hashlib
import logging

from google.appengine.api import images

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images
from models import Utilities,Passenger, Driver, Passenger_Request, Connected, Driver_Request

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
    
def count_connected_notifications(accepted_connections):
    count = 0
    if accepted_connections == None:
        return 0
    else:
        for e in accepted_connections:
            count += 1
        return count

def login(self, user, type):
    hash_id = make_id_hash(int(user.key().id()))
    set_cookie(self, 'id', hash_id)
    self.redirect('/' + type)


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
        self.render("new.html", error="")

    def post(self):
        action = self.request.get("action")
        if action == "Login":
            phone_number = self.request.get("phone_number")
            password = self.request.get("password")
            status, user = Utilities.check_user(self,phone_number,password)
            if status:
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                set_cookie(self, "detector", user.key())
                self.redirect('/passenger')
            else:
                error = "Invalid login details"
                self.render("new.html", error=error)

        elif action == "Create Account":
            email = self.request.get("email")
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            phone_number = self.request.get("new_phone_number")
            password = self.request.get("new_password")
            user_type = self.request.get("userOption")

            if user_type == 'passenger':
                status, user = Passenger.create_passenger(email, first_name,last_name, phone_number, password)
            else:
                status, user = Driver.create_driver(first_name,last_name, phone_number, password)

            if status:
                error = 'Phone number is already in use.'
                self.render("new.html", error=error)
            else:
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                set_cookie(self, "detector", user.key())
                self.redirect("/passenger")
#                % (int(user.key().id()))
        
class PassengerHandler(Handler):
    def get(self):
        error = self.request.get("error")
        key = self.request.cookies.get("detector")
        passenger = db.get(key)
        accepted_connections = Connected.gql("WHERE viewed = False")
        no_of_notifications = count_connected_notifications(accepted_connections)
        self.render("passenger.html", passenger = passenger, error = error, notifications = no_of_notifications, accepted_connections = accepted_connections)
        
    def post(self):
        key = self.request.cookies.get("detector")
        passenger = db.get(key)
        current_location = self.request.get("current_location")
        destination = self.request.get("destination")
        price_offer = self.request.get("price")
        info = self.request.get("other_info")
        
        error = "Please provide all required details"
        if passenger and current_location and destination and price_offer:
            request = Passenger_Request(passenger = passenger, current_location = current_location, destination = destination, price_offer = price_offer, other_info = info)
            
            request.put()
            self.render("success.html", passenger = passenger)
        else:
            self.redirect("/passenger?error=%s"%error)

#class DriverHandler(Handler):
#    def get(self):
#        self.render("driver.html")
#        login(self,user,user_type)


class Verification(Handler):
    def get(self):
        self.render('verify.html')


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
        company_name = self.request.cookies.get("c_name")
        company = Driver.gql("WHERE company_name = :1 ORDER BY created", company_name).get()
        passenger_requests = Passenger_Request.gql("ORDER BY created")
        self.render("driver_home.html", passenger_requests = passenger_requests, company = company)
        
    def post(self):
        response = self.request.get("response")
        
        if response == "Decline":
            message = self.request.get("message")
            self.redirect("/home")
        elif response == "OK":
            key = self.request.get("request_key")
            request = db.get(key)
            passenger = request.passenger
            driver_name = self.request.get("driver_name")
            driver = Driver.gql("WHERE first_name = :1", driver_name).get()
            message = self.request.get("message")
            
            new_connection = Connected(passenger = passenger, driver = driver, location = request.current_location, destination = request.destination,
                                       message = message)
            new_connection.put()
            request.processed = True
            self.redirect("/home")
        
            
        
class ImageHandler(Handler):
    def get(self):
        passenger = db.get(self.request.get('img_key'))
        if passenger.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.write(passenger.picture)

#        if state == 'logout':
#            delete_cookie(self, 'id')
#
#        if driver and current_location and destination:
#            request = Driver_Request(driver = driver, current_location = current_location, destination = destination)
#            request.put()
#        else:
#            currentUser = self.request.cookies.get("id")
#            if currentUser:
#                list = currentUser.split('|')
#                checkUser = check_id_hash(list[1])
#                if currentUser == checkUser:
#                    self.redirect("/%d" % (int(list[1])))


class VerifyUser(Handler):
    def get(self):
        phonenumber = self.request.get("phonenumber")
        password = self.request.get("password")
        status, user = Utilities.check_user(self,phonenumber,password)
        if status:
            hash_id = make_id_hash(int(user.key().id()))
            set_cookie(self, 'id', hash_id)
            set_cookie(self, "detector", user.key())
            self.write('verification success')
#            logging.info('user is valid')
        else:
#            logging.info('user is not valid')
            self.write('verification failed')
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/logout', SignupHandler),
    ('/signup', SignupHandler),
    ('/passenger', PassengerHandler),
    ('/driver', DriverHandler),
    ('/home', DriverHome),
    ('/img', ImageHandler),
    ('/verifyuser', VerifyUser)
    #('/verify', Verification)
], debug=True)
