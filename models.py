from google.appengine.ext import db

class Passenger(db.Model):
    first_name = db.StringProperty(required = True)
    last_name = db.StringProperty(required = True)
    phone_number = db.StringProperty(required = True)
    picture = db.BlobProperty()
    
class Passenger_Request(db.Model): #Might not be useful, still thinking through it
    passenger = db.ReferenceProperty(Passenger)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()
    destination = db.StringProperty(required = True)
    price_offer = db.StringProperty()
    other_info = db.TextProperty()
    
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
    
class Connected(db.Model):
    passenger = db.ReferenceProperty(Passenger)
    driver = db.ReferenceProperty(Driver)
    where = db.StringProperty(required = True)
    destination = db.StringProperty(required = True)
    
class Driver_Request(db.Model):
    driver = db.ReferenceProperty(Driver)
    current_location = db.StringProperty(required = True)
    current_location_latlng = db.StringProperty()
    destination = db.StringProperty(required = True)