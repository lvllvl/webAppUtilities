from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
# writing python classes that represent our forms 
# then theyll be converted to HTML

class RegistrationForm( FlaskForm ):

    username = StringField( 'Username', 
                    validators=[ DataRequired(), Length( min = 2, max=20) ] )
    email = StringField( 'Email', 
                    validators=[ DataRequired(), Email() ] )

    password = PasswordField( 'Passowrd', 
                    validators=[ DataRequired(), Length( min = 8, max = 20 )  ])

    confirm_password = PasswordField( 'Confirm Passowrd', 
                    validators=[ DataRequired(), EqualTo('password'))  ] )

    submit = SubmitField( 'Sign Up' ) 

class LoginForms( FlaskForm ):

    email = StringField( 'Email', 
                    validators=[ DataRequired(), Email() ] )

    password = PasswordField( 'Passowrd', 
                    validators=[ DataRequired(), Length( min = 8, max = 20 )  ])

    remember =  BooleanField( 'Remember Me' ) 
    submit = SubmitField( 'Login' ) 