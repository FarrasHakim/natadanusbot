from flaskblog import db
from sqlalchemy.types import ARRAY 

class nata_user(db.Model):
    id = db.Column('user_id', db.String(64), primary_key=True)
    user_line = db.Column('user_line', db.String(20))
    user_events = db.Column('user_events', ARRAY(db.String(10), dimensions=2), nullable=False, default=[])
    # confirmation input
    user_toggle = db.Column('user_toggle', db.Boolean, nullable=False, default=False)
    user_name = db.Column('user_name', db.String(64))
    user_email = db.Column('user_email', db.String(120))
    user_date = db.Column('user_date', db.String(10))
    user_image_link = db.Column('user_image_link', db.String(120))

    def __repr__(self):
        return f"nata_user('{self.user_line}')"

class cart(db.Model):
    id = db.Column('cart_id', db.Integer, primary_key=True)
    cart_id = db.Column('cart_userID', db.String(64), db.ForeignKey('nata_user.user_id'))
    cart_name = db.Column('cart_name', db.String(64))
    cart_email = db.Column('cart_email', db.String(120))
    cart_date = db.Column('cart_date', db.String(10))
    cart_events = db.Column('cart_orders', ARRAY(db.String(10), dimensions=2), nullable=False, default=[])
    cart_image_link = db.Column('cart_image_link', db.String(120))

    def __repr__(self):
        return f"cart('{self.cart_name}', '{self.cart_email}', '{self.cart_date}')"

class Event(db.Model):
    id = db.Column('event_id', db.String(10), primary_key=True)
    event_name = db.Column('event_name', db.String(50), nullable=False)
    event_price = db.Column('event_price', db.Integer, nullable=False)
    event_pvdr = db.Column('event_pvdr', db.String(50), nullable=False) 
    event_desc = db.Column('event_desc', db.Text , nullable=False)
    event_location = db.Column('event_location', db.String(50), nullable=False)
    event_count = db.Column('event_count', db.Integer, nullable=False, default=0)
    

    def __repr__(self):
        return f"event('{self.id}', '{self.event_name}', '{self.event_price}', '{self.event_pvdr}')"

    