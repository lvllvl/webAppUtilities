from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Properties, Tenant
from datetime import date, datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # create a custom validation 
    def validate_username( self, username ): 
        user = User.query.filter_by( username = username.data ).first() 
        if user : 
            raise ValidationError( 'That username is taken. Please choose a different one.' ) 

    def validate_email( self, email ): 
        email = User.query.filter_by( email = email.data ).first() 
        if email: 
            raise ValidationError( 'That email is taken. Please choose a different one.' ) 

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField( 'Update Profile Picture', validators=[ FileAllowed( ['jpg', 'png' ]) ])
    submit = SubmitField('Update')

    # create a custom validation 
    def validate_username( self, username ):
        if username.data != current_user.username: 
            user = User.query.filter_by( username = username.data ).first() 
            if user : 
                raise ValidationError( 'That username is taken. Please choose a different one.' ) 

    def validate_email( self, email ): 
        if email.data != current_user.email: 
            email = User.query.filter_by( email = email.data ).first() 
            if email: 
                raise ValidationError( 'That email is taken. Please choose a different one.' ) 

class PropertyForm( FlaskForm ): 

    # e.g., 7713 Street name 
    address = StringField( label='Address', validators=[ DataRequired() ] ) 
    zipCode = IntegerField( label='Zip Code', validators=[ DataRequired() ] )
    apartmentNo = StringField( label='Apartment Number, ( n/a if not applicable ) ', validators=[ DataRequired() ] )

    # TODO --> do you even need this feature?
    # state = SelectField( 'State', choices = [ 'Alabama', 'Alaska', 'Arizona', 
    #                      'Arkansas', 'California', 'Colorado', 'Connecticut', 
    #                      'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
    #                      'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
    #                      'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
    #                      'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 
    #                      'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
    #                      'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
    #                      'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
    #                      'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
    #                      'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 
    #                      'Wisconsin', 'Wyoming' ], validate_choice=True 
    #                      )
    submit = SubmitField( 'Save' )

# supports Tenant form
def choice_query(): 
    return Properties.query

class TenantForm( FlaskForm ): 

    first_name = StringField( label='First Name', validators=[ DataRequired() ])
    last_name = StringField( label='Last Name', validators=[ DataRequired() ])
    email = StringField( label = 'Email', validators=[ DataRequired() ] ) 
    deposit = IntegerField( label='Deposit Amount', validators=[ DataRequired() ])
    moveIn_date = DateField('Move-In Date', format="%m-%d-%Y", default=date.today ) 

    def_date = date( 9999, 9, 9 )
    moveOut_date = DateField('Move-Out Date', format="%m-%d-%Y", default= def_date ) 
    phone_number = IntegerField( label='Phone number', validators=[ DataRequired() ])
    
    # address will be imported from Property information ... can be left blank 
    property_address = QuerySelectField( query_factory= choice_query , allow_blank = False, get_label= 'address' ) 

    submit = SubmitField( 'Save' ) 

    # Validate if tenant already exists in your system by checking email
    # def validate_email( self, email ): 
    #     email =  Tenant.query.filter_by( email = email.data ).first() 
        
    #     if email: 
    #         raise ValidationError( 'That tenant already exists in your database. Please review your list of existing tenants.' ) 