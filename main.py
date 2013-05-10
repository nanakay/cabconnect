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
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

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
<<<<<<< HEAD


=======
    
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
def count_connected_notifications(accepted_connections):
    count = 0
    if accepted_connections == None:
        return 0
    else:
        for e in accepted_connections:
            count += 1
        return count

<<<<<<< HEAD

=======
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
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

<<<<<<< HEAD

class MainHandler(Handler):
    def get(self):
        self.redirect('/admin')

=======
class MainHandler(Handler):
    def get(self):
        self.redirect('/signup')
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f

class SignupHandler(Handler):
    def get(self):
        self.render("index.html", error="")

    def post(self):
        action = self.request.get("action")
        if action == "Login":
            phone_number = self.request.get("phone_number")
            password = self.request.get("password")
            status, user = Utilities.check_user(self, phone_number, password)
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
                status, user = Passenger.create_passenger(email, first_name, last_name, phone_number, password)
            else:
                status, user = Driver.create_driver(first_name, last_name, phone_number, password)

            if status:
                error = 'Phone number is already in use.'
                self.render("new.html", error=error)
            else:
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                set_cookie(self, "detector", user.key())
                self.redirect("/passenger")
<<<<<<< HEAD

# % (int(user.key().id()))

=======
#                % (int(user.key().id()))
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class PassengerHandler(Handler):
    def get(self):
        error = self.request.get("error")
        key = self.request.cookies.get("detector")
        passenger = db.get(key)
        accepted_connections = Connected.gql("WHERE viewed = False")
        no_of_notifications = count_connected_notifications(accepted_connections)
<<<<<<< HEAD
        self.render("passenger.html", passenger=passenger, error=error, notifications=no_of_notifications,
            accepted_connections=accepted_connections)

=======
        self.render("passenger.html", passenger=passenger, error=error, notifications=no_of_notifications, accepted_connections=accepted_connections)
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
    def post(self):
        key = self.request.cookies.get("detector")
        passenger = db.get(key)
        current_location = self.request.get("current_location")
        destination = self.request.get("destination")
        price_offer = self.request.get("price")
        info = self.request.get("other_info")
<<<<<<< HEAD

        error = "Please provide all required details"
        if passenger and current_location and destination and price_offer:
            request = Passenger_Request(passenger=passenger, current_location=current_location, destination=destination,
                price_offer=price_offer, other_info=info)

=======
        
        error = "Please provide all required details"
        if passenger and current_location and destination and price_offer:
            request = Passenger_Request(passenger=passenger, current_location=current_location, destination=destination, price_offer=price_offer, other_info=info)
            
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            request.put()
            self.render("success.html", passenger=passenger)
        else:
            self.redirect("/passenger?error=%s" % error)

<<<<<<< HEAD
=======
# class DriverHandler(Handler):
#    def get(self):
#        self.render("driver.html")
#        login(self,user,user_type)

>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f

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
<<<<<<< HEAD

=======
        
#         if driver and current_location and destination:
#             request = Driver_Request(driver = driver, current_location = current_location, destination = destination)
#             request.put()
#         else:
#             self.write("Fill it all out")
            
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class DriverHome(Handler):
    def get(self):
        company_name = self.request.cookies.get("c_name")
        company = Driver.gql("WHERE company_name = :1 ORDER BY created", company_name).get()
        passenger_requests = Passenger_Request.gql("ORDER BY created")
        self.render("driver_home.html", passenger_requests=passenger_requests, company=company)
<<<<<<< HEAD

    def post(self):
        response = self.request.get("response")

=======
        
    def post(self):
        response = self.request.get("response")
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
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
<<<<<<< HEAD
            new_connection = Connected(passenger=passenger, driver=driver, location=request.current_location,
                destination=request.destination,
                message=message)
            new_connection.put()
            request.processed = True
            self.redirect("/home")


=======
            
            new_connection = Connected(passenger=passenger, driver=driver, location=request.current_location, destination=request.destination,
                                       message=message)
            new_connection.put()
            request.processed = True
            self.redirect("/home")
        
            
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class ImageHandler(Handler):
    def get(self):
        passenger = db.get(self.request.get('img_key'))
        if passenger.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.write(passenger.picture)

<<<<<<< HEAD
=======
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
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
def to_json(query_obj):
    result = []
    for entry in query_obj:
        result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))
    return result

<<<<<<< HEAD

=======
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
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
<<<<<<< HEAD


def make_code():
    return ''.join(random.choice(string.letters) for x in xrange(5))


class CreateUser(Handler):
    def post(self):
        option = self.request.get("option")
=======
            
def make_code():
    return ''.join(random.choice(string.letters) for x in xrange(5))
        
class CreateUser(Handler):
    def post(self):
        option = self.request.get("option")
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        first_name = self.request.get("first_name")
        phone_number = self.request.get("phone_number")
        if option == "create_user":
            password = self.request.get("password")
            email = self.request.get("email")
            first_name = self.request.get("first_name")
            last_name = self.request.get("last_name")
<<<<<<< HEAD

            status, user = Passenger.create_passenger(first_name, last_name, phone_number, password, email)

            if status:
                self.write("Signup failed, Phone number " + phone_number + " is already in use")
            else:
            # self.write(phone_number + "," + password + "," + email)
=======
            
            status, user = Passenger.create_passenger(first_name, last_name, phone_number, password, email)
            
            if status:
                self.write("Signup failed, Phone number " + phone_number + " is already in use")
            else:
    #            self.write(phone_number + "," + password + "," + email)
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
                hash_id = make_id_hash(int(user.key().id()))
                set_cookie(self, 'id', hash_id)
                set_cookie(self, "detector", user.key())
                self.write(user.first_name)
<<<<<<< HEAD

        elif option == "verify_number":
            logging.info("sent phone number")
            code = make_code()

=======
        elif option == "verify_number":
            logging.info("sent phone number")
            code = make_code()
            
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            message = urllib.quote(u"Hi " + first_name + ", your number verification code is " + code + ". Please enter this to complete signup.".encode("utf-8"))
            name = urllib.quote(u"4apps".encode("utf-8"))
            
 #           action = urlfetch.Fetch("http://infoline.nandiclient.com/" + name + "/campaigns/sendCampaign/cabkonekt/cabkonekt/233249851596/"+message + "/" + name + "", validate_certificate = False)
            request = urlfetch.Fetch("https://infoline.nandiclient.com/" + name + "/campaigns/sendCampaign/cabkonekt/cabkonekt/" + phone_number + "/" + message)
            status = request.status_code
#             233277482171
#             action = urllib2.urlopen(request)
#             output = action.read()
            if status == 200:
                self.write(code)
            else:
                self.write("System failed to send code to you. Please try again")
<<<<<<< HEAD

=======
            
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
def create_date_object(date):
    the_date = datetime.strptime(date, "%Y-%m-%d")
    return the_date

<<<<<<< HEAD

def create_time_object(time):
    the_time = datetime.strptime(time, "%H:%M")
    return the_time


class Request(Handler):
    def post(self):
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

        request = Passenger_Request(passenger=passenger, location=location, destination=destination,
            from_date=from_date, to_date=to_date,
            pickup_time=pickup_time, to_time=to_time, total_passengers=total_passengers, other_info=other_info)

        request.put()
        self.write("successful")

class AdminLogin(Handler):
    def get(self):
        self.render('disp_login.html')

    def post(self):
        admin_email = self.request.get("email")
        admin_password = self.request.get("password")
        if admin_email and admin_password:
            status, object = Admin.check_admin(email=admin_email, password=admin_password)
            #            status, object = Admin.create_admin(first_name="Admin", last_name="User",phone_number='020666',email=admin_email, password=admin_password)
            if status:
                self.redirect('/admin_dashboard?options=Pending')
            else:
                error='"Invalid Login Details'
                self.render('disp_login.html', error=error)
        else:
            error="You didn't provide all details"
            self.render('disp_login.html', error=error)


class AdminHandler(Handler):
    def get(self):
        choice = self.request.get('options')
        pending = Passenger_Request.gql("WHERE status = :1 ORDER BY created DESC", "Pending")
        active = Passenger_Request.gql("WHERE status = :1 ORDER BY created DESC", "Active")
        completed = Passenger_Request.gql("WHERE status = :1 ORDER BY created DESC", "Completed")
        available = Driver.gql("WHERE available = True")

        if choice == "Pending":
            holder = pending
        elif choice == "Active":
            holder = active
        elif choice =="Completed":
            holder = completed
        elif choice =="Available":
            holder = available
        else:
            holder = pending
        self.render("disp_dashboard.html", holder = holder, pending = pending.count(), active = active.count(),available=available.count())
        #        feedbacks = Feedback.gql("ORDER BY created ASC")


    def post(self):
        config = self.request.get("config")
        if config == "Add Driver":
=======
def create_time_object(time):
    the_time = datetime.strptime(time, "%H:%M")
    return the_time
            
class Request(Handler):
    def post(self):
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
            
            request = Passenger_Request(passenger=passenger, location=location, destination=destination, from_date=from_date, to_date=to_date,
                pickup_time=pickup_time, to_time=to_time, total_passengers=total_passengers, other_info=other_info)
            
            if request:
                request.put()
                self.write("successful")
            else:
                self.write("It failed")
                  
            
class AdminHandler(Handler):
    def get(self):
        pending_requests = Passenger_Request.gql("WHERE status = :1", "Pending")
        
        feedbacks = Feedback.gql("ORDER BY created ASC")
        available_drivers = Driver.gql("WHERE available = True")
        
        self.render("dispatch.html", pending_requests=pending_requests, available_drivers=available_drivers, feedbacks=feedbacks)
        
    def post(self):
        option = self.request.get("option")
        
        if option == "add_driver":
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            first_name = self.request.get("driver_first_name")
            last_name = self.request.get("driver_last_name")
            password = self.request.get("driver_password")
            phone_number = self.request.get("driver_p_number")
<<<<<<< HEAD
#            picture = self.request.get("picture")

#            if not picture:
            picture = db.Blob(urlfetch.Fetch("https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif").content)
            status, user = Driver.create_driver(first_name, last_name, phone_number, password,picture)

=======
            
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            status, user = Driver.create_driver(first_name, last_name, phone_number, password)

            if status:
                self.write('You cannot create two accounts with the same number')
            else:
<<<<<<< HEAD
#                hash_id = make_id_hash(int(user.key().id()))
                msg = " Driver added successfully"
                self.render('disp_dashboard.html', msg=msg)

        elif config == "Add Admin":
            first_name = self.request.get("admin_first_name")
            last_name = self.request.get("admin_last_name")
            email = self.request.get("admin_email")
            password = self.request.get("admin_password")
            phone_number = self.request.get("admin_p_number")
            status, user = Admin.create_admin(first_name, last_name, email,phone_number, password)

            if status:
                self.write('You cannot create two accounts with the same number')
            else:
                msg = " Admin added successfully"
                self.render('disp_dashboard.html', msg=msg)

        elif config == "assign_driver":
=======
                hash_id = make_id_hash(int(user.key().id()))
                self.write(" Driver added successfully")
        elif option == "assign_driver":
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            first_name = self.request.get("driver_first_name")
            last_name = self.request.get("driver_last_name")
            message = self.request.get("message")
            key = self.request.get("request_key")
<<<<<<< HEAD

            driver = db.GqlQuery("SELECT * FROM Driver WHERE first_name=:1 AND last_name=:2", first_name,
                last_name).get()
            driver.available = False
            driver.put()
            #
=======
            
#             driver = Driver.gql("WHERE first_name = :1 AND last_name = :2", (first_name, last_name)).get()
            driver = db.GqlQuery("SELECT * FROM Driver WHERE first_name=:1 AND last_name=:2", first_name, last_name).get()
            driver.available = False
            driver.put()
#             
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            request = db.get(key)
            logging.info(request)
            request.status = "Active"
            request.assigned_driver = driver
            request.put()
<<<<<<< HEAD
            #
            self.write("successful")



def get_date(date_object):
# day = date_object.day
# month = date_object.month
# year = date_object.year
#
# date = str(day) + " " + str(month) + " " + str(year)
    date = date_object.strftime("%d %b, %Y")
    return date


def get_time(time_object):
    return time_object.strftime("%H : %M")


def history_toJson(requests):
    history = []
    history_obj = {}
#    for request in requests:
=======
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
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
#     day = date_object.day
#     month = date_object.month
#     year = date_object.year
#     
#     date = str(day) + " " + str(month) + " " + str(year)
<<<<<<< HEAD
#    date = date_object.strftime("%d %b, %Y")
#    return date
=======
    date = date_object.strftime("%d %b, %Y")
    return date
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f

def get_time(time_object):
    return time_object.strftime("%H : %M")
 
def history_toJson(requests):
    
    history_obj = {}
    for request in requests:
        history = []
        history_obj['request_date'] = get_date(request.created)
        history_obj['request_location'] = request.location
        history_obj['request_destination'] = request.destination
        history_obj['request_from_date'] = get_date(request.from_date)
        history_obj['request_to_date'] = get_date(request.to_date)
        history_obj['request_from_time'] = get_time(request.pickup_time)
        history_obj['request_to_time'] = get_time(request.to_time)
        history_obj['request_from_date'] = get_date(request.from_date)
        history_obj['request_status'] = request.status
<<<<<<< HEAD

        history.append(history_obj)

    history_json = json.dumps(history)
    return history_json

class AdminCars(Handler):
    def get(self):
        self.render('disp_cars.html')

=======
        
        history.append(history_obj)
        
    history_json = json.dumps(history)
    return history_json
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class HistoryHandler(Handler):
    def get(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
<<<<<<< HEAD

        requests = Passenger_Request.gql("WHERE passenger = :1", passenger)
=======
        
        requests = Passenger_Request.gql("WHERE passenger = :1", passenger)
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        history = history_toJson(requests)
        logging.info("This is history in json " + history)
        if history is None:
            self.write("empty")
        else:
            self.write(history)
<<<<<<< HEAD

=======
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class FeedbackHandler(Handler):
    def post(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number).get()
<<<<<<< HEAD

=======
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        price_rating = self.request.get("price_rating")
        punctuality_rating = self.request.get("punctuality_rating")
        security_rating = self.request.get("security_rating")
        care_rating = self.request.get("care_rating")
        standard_rating = self.request.get("standard_rating")
        message = self.request.get("message")
<<<<<<< HEAD

        feedback = Feedback(passenger=passenger, price_rating=price_rating, punctuality_rating=punctuality_rating,
            security_rating=security_rating, care_rating=care_rating, standard_rating=standard_rating, message=message)

        feedback.put()

=======
        
        feedback = Feedback(passenger=passenger, price_rating=price_rating, punctuality_rating=punctuality_rating, security_rating=security_rating, care_rating=care_rating, standard_rating=standard_rating, message=message)
        feedback.put()
        
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        self.write("successful")
        
def update_attribute(transaction):
    for entity in transaction:
        entity.viewed = True
        entity.put()
 
def new_toJson(transactions):
    update_obj = []
     
    for entity in transactions:
        entity_obj = {}
        entity_obj["passenger"] = entity.passenger.first_name + " " + entity_obj.passenger.last_name
        entity_obj["location"] = entity.request.location
        entity_obj["destination"] = entity.request.destination
        entity_obj["location"] = entity.request.location
        entity_obj["from_date"] = entity.request.from_date
        entity_obj["to_date"] = entity.request.to_date
        entity_obj["pickup_time"] = entity.request.pickup_time
        entity_obj["to_time"] = entity.request.to_time
        entity_obj["driver"] = entity.driver.first_name + " " + entity_obj.driver.last_name
        
        update_obj.append(entity_obj)
    
    json_update = json.dumps(update_obj)
    return json_update
        
class UpdateHandler(Handler):
    def get(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number)
        
        newTransactions = Transaction.gql("WHERE passenger = :1 AND viewed = False", passenger)
        
        if newTransactions:
            update_attribute(newTransactions)
            
            json_obj = new_toJson(newTransactions)
            self.write(json_obj)
        else:
            self.write("empty")

<<<<<<< HEAD
def update_attribute(transaction):
    for entity in transaction:
        entity.viewed = True
        entity.put()

def new_toJson(transactions):
    update_obj = []

    for entity in transactions:
        entity_obj = {}
        entity_obj["passenger"] = entity.passenger.first_name + " " + entity_obj.passenger.last_name
        entity_obj["location"] = entity.request.location
        entity_obj["destination"] = entity.request.destination
        entity_obj["location"] = entity.request.location
        entity_obj["from_date"] = entity.request.from_date
        entity_obj["to_date"] = entity.request.to_date
        entity_obj["pickup_time"] = entity.request.pickup_time
        entity_obj["to_time"] = entity.request.to_time
        entity_obj["driver"] = entity.driver.first_name + " " + entity_obj.driver.last_name

        update_obj.append(entity_obj)

    json_update = json.dumps(update_obj)
    return json_update

class UpdateHandler(Handler):
    def get(self):
        phone_number = self.request.get("phone_number")
        passenger = Passenger.gql("WHERE phone_number = :1", phone_number)

        newTransactions = Transaction.gql("WHERE passenger = :1 AND viewed = False", passenger)

        if newTransactions:
            update_attribute(newTransactions)

            json_obj = new_toJson(newTransactions)
            self.write(json_obj)
        else:
            self.write("empty")

=======
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
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
<<<<<<< HEAD
    ('/admin', AdminLogin),
    ('/admin_dashboard', AdminHandler),
    ('/admin_cars', AdminCars),
=======
    ('/admin', AdminHandler),
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
    ('/history', HistoryHandler),
    ('/feedback', FeedbackHandler),
    ('update', UpdateHandler)
], debug=True)
