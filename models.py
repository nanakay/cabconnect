from google.appengine.ext import db

import random
import string
import hashlib

from google.appengine.api import urlfetch

def make_salt():
    return ''.join(random.choice(string.letters) for i in range(5))
class Utilities(db.Model):
    @staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for i in range(5))

    @staticmethod
    def make_pw_hash(password):
        salt = Utilities.make_salt()
        pw_hash = password + salt
        return hashlib.sha256(pw_hash).hexdigest() + salt, salt

    @staticmethod
    def check_pw_hash(password, user):
        pw_hash = password + user.salt
        hashed = hashlib.sha256(pw_hash).hexdigest() + user.salt
        if hashed == user.password:
            return True
        else:return False

    @staticmethod
    def userExists(userExists,phone_number):
        return userExists.filter("phone_number =", phone_number)

    @staticmethod
    def check_user(self, phone_number, password):
        passengerExists = Passenger.all()
        find = Utilities.userExists(passengerExists,phone_number)
        found = find.get()
        if found:
            check = Utilities.check_pw_hash(password, found)
            if check:
                return True, found
            else:
                return False, found
        else:
            driverExists = Driver.all()
            find = Utilities.userExists(driverExists,phone_number)
            found = find.get()
            if found:
                check = Utilities.check_pw_hash(password, found)
                if check:
                    return True, found
                else:
                    return False, found
        return False, found

class Passenger(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    password = db.TextProperty(required=True)
    phone_number = db.StringProperty(required = True)
    email = db.EmailProperty()
    picture = db.BlobProperty()
    salt = db.StringProperty()

    @classmethod
    def create_passenger(cls, first_name, last_name, phone_number, password, email):
        passengerExists = Passenger.all()
        passengerExists = passengerExists.filter('phone_number =', phone_number)
        find = passengerExists.get()
        if find:
            return True, find
        else:
            password, salt= Utilities.make_pw_hash(password)
            newPassenger = Passenger(first_name = first_name, last_name = last_name, password=password, phone_number=phone_number, email=email, salt=salt)
            newPassenger.picture = db.Blob(urlfetch.Fetch("https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif").content)
            newPassenger.put()
            return False, newPassenger

#    @classmethod
#    def check_passenger(cls, phone_number, password):
#        passengerExists = Passenger.all()
#        find = passengerExists.filter("phone_number =", phone_number)
#        found = find.get()
#        if found:
#            hash = check_pw_hash(password, found.salt)
#            userspass = found.password
#            if hash == userspass:
#                return True, found
#            else:
#                return False, found
#        else:
#            return False, found


    
class Driver(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    phone_number = db.StringProperty(required = True)
    password = db.StringProperty(required=True)
    picture = db.BlobProperty()
    available = db.BooleanProperty(default = True)
    salt = db.StringProperty()

    @classmethod
    def create_driver(cls,first_name,last_name, phone_number, password):
        driverExists = Driver.all()
        driverExists = driverExists.filter('phone_number =', phone_number)
        find = driverExists.get()
        if find:
            return True, find
        else:
            password, salt= Utilities.make_pw_hash(password)
            newDriver= Driver(first_name = first_name, last_name = last_name, password=password, phone_number=phone_number,salt=salt)
            newDriver.picture = db.Blob(urlfetch.Fetch("https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif").content)
            newDriver.put()
        return False, newDriver

class Passenger_Request(db.Model): #Might not be useful, still thinking through it
    passenger = db.ReferenceProperty(Passenger)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()
    destination = db.StringProperty(required = True)
    other_info = db.TextProperty()
    assigned_driver = db.ReferenceProperty(Driver)
    created = db.DateTimeProperty(auto_now_add = True)
    pickup_time = db.StringProperty(required = True)
    timeframe = db.StringProperty()
    status = db.StringProperty(default = "Pending")
    
class Passenger_Reserve(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    location = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    other_info = db.TextProperty()
    assigned_driver = db.ReferenceProperty(Driver)
    created = db.DateTimeProperty(auto_now_add = True)
    pickup_time = db.StringProperty(required = True)
    to_time = db.StringProperty()
    status = db.StringProperty(default = "Pending")
    

class Connected(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    driver = db.ReferenceProperty(Driver)
    location = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    price = db.StringProperty()
    message = db.TextProperty()
    viewed = db.BooleanProperty(default = False)


class Driver_Request(db.Model):
    driver = db.ReferenceProperty(Driver)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()

class Admin(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    picture = db.BlobProperty()
