import webapp2
import jinja2
import re
import hashlib
import logging
import json
from datetime import datetime
import random
import urllib2
import string
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import images
from models import *

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
        self.redirect('/signup')

class SignupHandler(Handler):
    def get(self):
        self.render("dispatch.html", error="")

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
def to_json(query_obj):
    result = []
    for entry in query_obj:
        result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))
    return result

class VerifyUser(Handler):
    def post(self):
        phonenumber = self.request.get("phonenumber")
        password = self.request.get("password")
        status, user = Utilities.check_user(self, phonenumber, password)
        if status:
            hash_id = make_id_hash(int(user.key().id()))
            set_cookie(self, 'id', hash_id)
            set_cookie(self, "detector", user.key())

            self.write(user.first_name)
        else:
            self.write('Verification failed')
            
def make_code():
    return ''.join(random.choice(string.letters) for x in xrange(5))
        
class CreateUser(Handler):
    def post(self):
        option = self.request.get("option")
        
        phone_number = self.request.get("phone_number")
        if option == "create_user":
            password = self.request.get("password")
            email = self.request.get("email")
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
            
            status, user = Passenger.create_passenger(first_name, last_name, phone_number, password, email)
            
            if status:
                self.write("Signup failed, Phone number " + phone_number + " is already in use")
            else:
    #            self.write(phone_number + "," + password + "," + email)
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                set_cookie(self, "detector", user.key())
                self.write(user.first_name)
        elif option == "verify_number":
            #logging.info("sent phone number")
            code = make_code()
            
            message = urllib.quote(u"Hi, your number verification code is " + code + ". Please enter this to complete signup.".encode("utf-8"))
            name = urllib.quote(u"Cab Konekt".encode("utf-8"))
            
 #           action = urlfetch.Fetch("http://infoline.nandiclient.com/" + name + "/campaigns/sendCampaign/cabkonekt/cabkonekt/233249851596/"+message + "/" + name + "", validate_certificate = False)
            request = urllib2.Request("http://infoline.nandiclient.com/" + name + "/campaigns/sendCampaign/cabkonekt/cabkonekt/233249851596/"+ message +"/")
# #            request = urllib2.Request("google.com.gh")
            action = urllib2.urlopen(request)
#             logging.info("action")
            output = action.read()
            logging.info("This is the output: " + output)
            self.write(output)
            
def create_date_object(date):
    the_date = datetime.strptime(date, "%Y-%m-%d")
    return the_date

def create_time_object(time):
    the_time = datetime.strptime(time, "%H:%M")
    return the_time
            
class Request(Handler):
    def post(self):
        option = self.request.get("option")
        if option == "request_cab":
            phone_number = self.request.get("phone_number")
            passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
            
            current_location = self.request.get("current_location")
            destination = self.request.get("destination")
            time = self.request.get("time")
            pickup_time = create_time_object(time)
            other_info = self.request.get("other_info")
            
            request = Passenger_Request(passenger = passenger, current_location = current_location, destination = destination, 
                                        pickup_time = pickup_time, other_info = other_info)
            if request:
                request.put()
                self.write("successful")
            else:
                self.write("request failed")
        elif option == "reserve_cab":
            phone_number = self.request.get("phone_number")
            passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
            
            location = self.request.get("current_location")
            destination = self.request.get("destination")
            
            date = self.request.get("from_date")
            from_date = create_date_object(date)
            
            another_date = self.request.get("to_date")
            to_date = create_date_object(another_date)
            
            time = self.request.get("reserve_pickup_time")
            pickup_time = create_time_object(time)
            
            another_time = self.request.get("to_time")
            to_time = create_time_object(another_time)
            
            total_passengers = self.request.get("total_passengers")
            other_info = self.request.get("reserve_other_info")
            
            reserve = Passenger_Reserve(passenger = passenger, location = location, destination = destination, from_date = from_date, to_date = to_date,
                pickup_time = pickup_time, to_time = to_time, total_passengers = total_passengers, other_info = other_info)
            
            reserve.put()
            self.write("successful")
                  
            
class AdminHandler(Handler):
    def get(self):
        pending_reserves = Passenger_Reserve.gql("WHERE status = :1", "Pending")
        pending_requests = Passenger_Request.gql("WHERE status = :1", "Pending")
        
        feedbacks = Feedback.gql("ORDER BY created ASC")
        available_drivers = Driver.gql("WHERE available = True")
        
        self.render("dispatch.html", pending_requests = pending_requests, available_drivers = available_drivers, feedbacks = feedbacks, pending_reserves = pending_reserves)
        
    def post(self):
        option = self.request.get("option")
        
        if option == "add_driver":
            first_name = self.request.get("driver_first_name")
            last_name = self.request.get("driver_last_name")
            password = self.request.get("driver_password")
            phone_number = self.request.get("driver_p_number")
            
            status, user = Driver.create_driver(first_name,last_name, phone_number, password)

            if status:
                self.write('You cannot create two accounts with the same number')
            else:
                hash_id = make_id_hash(int(user.key().id()))
                self.write(" Driver added successfully")
        elif option == "assign_driver":
            first_name = self.request.get("driver_first_name")
            last_name = self.request.get("driver_last_name")
            message = self.request.get("message")
            key = self.request.get("request_key")
            
#             driver = Driver.gql("WHERE first_name = :1 AND last_name = :2", (first_name, last_name)).get()
            driver = db.GqlQuery("SELECT * FROM Driver WHERE first_name=:1 AND last_name=:2", first_name, last_name).get()
            driver.available = False
            driver.put()
#             
            request = db.get(key)
            logging.info(request)
            request.status = "Active"
            request.assigned_driver = driver
            request.put()
#             
            self.write("successful")
#            first_name = self.request.get("first_name")
#            last_name = self.request.get("last_name")
#            password = self.request.get("password")
#            email = self.request.get("email")
#        if first_name and last_name and password:
#            admin = Admin(first_name = first_name, last_name = last_name, password = password)
#            admin.put()

def get_date(date_object):
    day = date_object.day
    month = date_object.month
    year = date_object.year
    
#     date = str(day) + " " + str(month) + " " + str(year)
    date = date_object.strftime("%d %b, %Y")
    return date
 
def history_toJson(requests, reserves):
    history = []
    history_obj = {}
    for request in requests:
        history_obj['driver'] = request.assigned_driver.first_name + " " + request.assigned_driver.last_name
        history_obj['request_date'] = get_date(request.created)
        history_obj['request_location'] = request.current_location
        history_obj['request_destination'] = request.destination
        history.append(history_obj)
        
    for reserve in reserves:
        history_obj['driver'] = reserve.assigned_driver.first_name + " " + reserve.assigned_driver.last_name
        history_obj['date'] = reserve.date
        history_obj['reserve_date'] = get_date(reserve.from_date)
        history_obj['to_date'] = get_date(reserve.to_date)
        history_obj['location'] = reserve.location
        history_obj['destination'] = reserve.destination
        history.append(history_obj)
        
    history_json = json.dumps(history)
    return history_json
        
class HistoryHandler(Handler):
    def get(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
        
        requests = Passenger_Request.gql("WHERE passenger = :1", passenger)
        reserves = Passenger_Reserve.gql("WHERE passenger = :1", passenger)
        
        history = history_toJson(requests, reserves)
        
        self.write(history)
        
class FeedbackHandler(Handler):
    def post(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
        
        price_rating = self.request.get("price_rating")
        punctuality_rating = self.request.get("punctuality_rating")
        security_rating = self.request.get("security_rating")
        care_rating = self.request.get("care_rating")
        standard_rating = self.request.get("standard_rating")
        message = self.request.get("message")
        
        feedback = Feedback(passenger = passenger, price_rating = price_rating, punctuality_rating = punctuality_rating, security_rating = security_rating, care_rating = care_rating, standard_rating = standard_rating, message = message)
        feedback.put()
        
        self.write("successful")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/logout', SignupHandler),
    ('/signup', SignupHandler),
    ('/passenger', PassengerHandler),
    ('/driver', DriverHandler),
    ('/home', DriverHome),
    ('/img', ImageHandler),
    ('/verifyuser', VerifyUser),
    ('/createuser', CreateUser),
    ('/request', Request),
    ('/admin', AdminHandler),
    ('/history', HistoryHandler),
    ('/feedback', FeedbackHandler)
], debug=True)
