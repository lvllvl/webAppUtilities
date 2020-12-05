from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForms
app = Flask( __name__ )
app.config[ 'SECRET_KEY' ] = '9e7b85843b7eff56c6341c89b2d1fcec' 

app.config[ "TEMPLATES_AUTO_RELOAD"] = True 
posts = [
    {
        'author': 'c shafer',
        'title': 'blog post 1',
        'content': "first post content",
        'date_posted': 'April 20, 2018'
    }, 
        {
        'author': 'Jane Doe',
        'title': 'Blog post 2 ',
        'content': "second post content",
        'date_posted': 'April 28, 2018'
    }
    
]
@app.route("/") 
@app.route("/home") # this is a route , decorator 
def home(): 
    return render_template( 'home.html', posts = posts ) 

@app.route("/about") # this is a route , decorator 
def about(): 
    return render_template( 'about.html', title = 'About' )  

@app.route("/register") # this is a route , decorator 
def register():
    form = RegistrationForm()
    return render_template( 'register.hmtl', title='Register', form = form ) 


@app.route("/login") # this is a route , decorator 
def login():
    form = LoginForms()
    return render_template( 'login.hmtl', title='Login', form = form ) 

if __name__ == '__main__':
    app.run( debug = True )