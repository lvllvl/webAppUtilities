from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user( user_id ): 
    return User.query.get( int( user_id )) 

class User( db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Properties( db.Model ):

    id = db.Column( db.Integer, primary_key=True )
    address = db.Column( db.Integer, nullable=False ) 
    street = db.Column( db.String, nullable=False ) 
    apartment = db.Column( db.Integer, nullable=False ) 
    state = db.Column( db.String( 50 ), nullable = False ) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return f"Properties('{self.address + self.street}' )"

class Tenant( db.Model ): 

    id = db.Column( db.Integer, primary_key=True )
    first_name = db.Column( db.String, nullable=False )
    last_name = db.Column( db.String, nullable=False )
    tenant_email = db.Column( db.String, unique=True, nullable=False )
    deposit_amount = db.Column( db.Integer, nullable=False )
    moveIn_date = db.Column( db.DateTime, default=datetime.datetime.utcnow, nullable=False )
    moveOut_date = db.Column( db.DateTime, default=datetime.datetime.utcnow, nullable=True )

    # TODO should this be a double instead of an integer????? 
    phone_number = db.Column( db.Integer, nullable = False ) 
    # TODO --> is this foreign key formatted correctly?  
    property_address = db.Column( db.Integer, db.ForeignKey( 'property.id' ), nullable=False ) 


    def __repr__( self ): 
        return f"Tenant( '{self.first_name + self.last_name}', '{sel.tenant_email}') '"