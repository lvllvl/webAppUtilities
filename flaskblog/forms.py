from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

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

    addressNo = IntegerField( label='Address Number', validators=[ DataRequired() ] ) 
    streetName = StringField( label='Street Name', validators=[ DataRequired() ] )
    zipCode = IntegerField( label='Zip Code', validators=[ DataRequired() ] )
    apartmentNo = StringField( label='Apartment Number, ( n/a if not applicable ) ', validators=[ DataRequired() ] )

    state = SelectField( 'State', choices = [ 'Alabama', 'Alaska', 'Arizona', 
                         'Arkansas', 'California', 'Colorado', 'Connecticut', 
                         'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
                         'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
                         'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
                         'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 
                         'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
                         'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
                         'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                         'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
                         'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 
                         'Wisconsin', 'Wyoming' ], validate_choice=True 
                         )

    submit = SubmitField( 'Save' )