from google.appengine.ext import db

import random
import string
import hashlib

from google.appengine.api import urlfetch

def make_salt():
    return ''.join(random.choice(string.letters) for i in range(5))
<<<<<<< HEAD


=======
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
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
<<<<<<< HEAD
        else: return False

    @staticmethod
    def userExists(userExists, phone_number):
=======
        else:return False

    @staticmethod
    def userExists(userExists,phone_number):
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        return userExists.filter("phone_number =", phone_number)

    @staticmethod
    def check_user(self, phone_number, password):
        passengerExists = Passenger.all()
<<<<<<< HEAD
        find = Utilities.userExists(passengerExists, phone_number)
=======
        find = Utilities.userExists(passengerExists,phone_number)
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        found = find.get()
        if found:
            check = Utilities.check_pw_hash(password, found)
            if check:
                return True, found
            else:
                return False, found
        else:
            driverExists = Driver.all()
<<<<<<< HEAD
            find = Utilities.userExists(driverExists, phone_number)
=======
            find = Utilities.userExists(driverExists,phone_number)
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            found = find.get()
            if found:
                check = Utilities.check_pw_hash(password, found)
                if check:
                    return True, found
                else:
                    return False, found
        return False, found

<<<<<<< HEAD

class Passenger(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    password = db.TextProperty(required=True)
    phone_number = db.StringProperty(required=True)
    email = db.EmailProperty()
    picture = db.BlobProperty()
    salt = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

=======
class Passenger(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    password = db.TextProperty(required=True)
    phone_number = db.StringProperty(required = True)
    email = db.EmailProperty()
    picture = db.BlobProperty()
    salt = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
    @classmethod
    def create_passenger(cls, first_name, last_name, phone_number, password, email):
        passengerExists = Passenger.all()
        passengerExists = passengerExists.filter('phone_number =', phone_number)
        find = passengerExists.get()
        if find:
            return True, find
        else:
<<<<<<< HEAD
            password, salt = Utilities.make_pw_hash(password)
            newPassenger = Passenger(first_name=first_name, last_name=last_name, password=password,
                phone_number=phone_number, email=email, salt=salt)
            newPassenger.picture = db.Blob(urlfetch.Fetch(
                "https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif").content)
            newPassenger.put()
            return False, newPassenger

# @classmethod
# def check_passenger(cls, phone_number, password):
# passengerExists = Passenger.all()
# find = passengerExists.filter("phone_number =", phone_number)
# found = find.get()
# if found:
# hash = check_pw_hash(password, found.salt)
# userspass = found.password
# if hash == userspass:
# return True, found
# else:
# return False, found
# else:
# return False, found



class Driver(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    phone_number = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    picture = db.BlobProperty()
    available = db.BooleanProperty(default=True)
    salt = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_driver(cls, first_name, last_name, phone_number, password, picture):
=======
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
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def create_driver(cls,first_name,last_name, phone_number, password):
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
        driverExists = Driver.all()
        driverExists = driverExists.filter('phone_number =', phone_number)
        find = driverExists.get()
        if find:
            return True, find
        else:
<<<<<<< HEAD
            password, salt = Utilities.make_pw_hash(password)
            newDriver = Driver(first_name=first_name, last_name=last_name, password=password, phone_number=phone_number,
                salt=salt, picture=picture)
=======
            password, salt= Utilities.make_pw_hash(password)
            newDriver= Driver(first_name = first_name, last_name = last_name, password=password, phone_number=phone_number,salt=salt)
            newDriver.picture = db.Blob(urlfetch.Fetch("https://fbcdn-profile-a.akamaihd.net/static-ak/rsrc.php/v2/yo/r/UlIqmHJn-SK.gif").content)
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
            newDriver.put()
        return False, newDriver

class Passenger_Request(db.Model):
    passenger = db.ReferenceProperty(Passenger)
<<<<<<< HEAD
    location = db.StringProperty(required=True)
    destination = db.StringProperty(required=True)
    other_info = db.TextProperty()
    assigned_driver = db.ReferenceProperty(Driver)
=======
    location = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    other_info = db.TextProperty()
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
    from_date = db.DateTimeProperty(required = True)
    to_date = db.DateTimeProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    pickup_time = db.DateTimeProperty(required = True)
    to_time = db.DateTimeProperty()
<<<<<<< HEAD
    status = db.StringProperty(default="Pending")
    total_passengers = db.StringProperty()

    @classmethod
    def create_request(cls, passenger):
        newRequest = Passenger_Request(passenger=passenger, location="Accra", destination="Lapaz Toyota")
        newRequest.put()
        return True

class Transaction(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    driver = db.ReferenceProperty(Driver)
    location = db.StringProperty(required=True)
    destination = db.StringProperty(required=True)
    price = db.StringProperty()
    message = db.TextProperty()
    viewed = db.BooleanProperty(default=False)
=======
    status = db.StringProperty(default = "Pending")
    total_passengers = db.StringProperty()
    
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f

class Transaction(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    driver = db.ReferenceProperty(Driver)
    request = db.ReferenceProperty(Passenger_Request)
    message = db.TextProperty()
<<<<<<< HEAD
    request = db.ReferenceProperty(Passenger_Request)
    message = db.TextProperty()
    viewed = db.BooleanProperty(default = False)

class Admin(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    phone_number = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    picture = db.BlobProperty()
    salt = db.StringProperty(required=True)

    @classmethod
    def create_admin(cls, first_name, last_name,email, phone_number, password):
        adminExists = Admin.gql('WHERE first_name =:1 AND last_name =:2', first_name, last_name).get()
        if adminExists:
            return True, adminExists
        else:
            password, salt = Utilities.make_pw_hash(password)
            newAdmin = Admin(first_name=first_name, last_name=last_name, password=password, salt=salt,
                phone_number=phone_number, email=email)
            newAdmin.put()
        return False, newAdmin

    @classmethod
    def check_admin(cls, email, password):
        adminExists = Admin.gql('WHERE email =:1', email).get()
        if adminExists:
            check = Utilities.check_pw_hash(password, adminExists)
            if check:
                return True, adminExists
            else:
                return False, adminExists
        else:
            return False, adminExists


=======
    viewed = db.BooleanProperty(default = False)

class Admin(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    picture = db.BlobProperty()
    
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
class Feedback(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    price_rating = db.StringProperty()
    punctuality_rating = db.StringProperty()
    security_rating = db.StringProperty()
    care_rating = db.StringProperty()
    standard_rating = db.StringProperty()
    message = db.TextProperty()
<<<<<<< HEAD
    created = db.DateTimeProperty(auto_now_add=True)
=======
    created = db.DateTimeProperty(auto_now_add = True)
 
>>>>>>> 2e6e5040bd86f2ce0b23e38caf786505c07cf95f
