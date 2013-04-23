from google.appengine.ext import db

import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.letters) for i in range(5))

def make_pw_hash(password):
    salt = make_salt()
    pw_hash = password + salt
    return hashlib.sha256(pw_hash).hexdigest() + salt, salt

def check_pw_hash(password, salt):
    pw_hash = password + salt
    return hashlib.sha256(pw_hash).hexdigest() + salt

class Passenger(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    password = db.TextProperty(required=True)
    phone_number = db.StringProperty(required = True)
    email = db.EmailProperty()
    picture = db.BlobProperty()
    salt = db.StringProperty()

    @classmethod
    def create_passenger(cls, email, first_name,last_name, phone_number, password):
        passengerExists = Passenger.all()
        passengerExists = passengerExists.filter('phone_number =', phone_number)
        find = passengerExists.get()
        if find:
            return True, find
        else:
            password, salt= make_pw_hash(password)
            newPassenger = Passenger(first_name = first_name, last_name = last_name,email=email, password=password, phone_number=phone_number,salt=salt)
            newPassenger.put()
            return False, newPassenger

    @classmethod
    def check_passenger(cls, phone_number, password):
        passengerExists = Passenger.all()
        find = passengerExists.filter("phone_number =", phone_number)
        found = find.get()
        if found:
            hash = check_pw_hash(password, found.salt)
            userspass = found.password
            if hash == userspass:
                return True, found
            else:
                return False, found
        else:
            return False, found

class Passenger_Request(db.Model): #Might not be useful, still thinking through it
    passenger = db.ReferenceProperty(Passenger)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()
    destination = db.StringProperty(required = True)
    price_offer = db.StringProperty()
    other_info = db.TextProperty()
    created = db.DateTimeProperty(required=True)
    
class Driver(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    phone_number = db.StringProperty(required = True)
    additional_number = db.StringProperty()
    car_number = db.StringProperty(required = True)
    car_description = db.StringProperty(required = True)
    picture = db.BlobProperty()
    station = db.StringProperty(required = True)
    online = db.BooleanProperty(default = False)
    verify= db.StringProperty()
    
class Connected(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    driver = db.ReferenceProperty(Driver)
    location = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    price = db.StringProperty()


class Driver_Request(db.Model):
    driver = db.ReferenceProperty(Driver)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()
