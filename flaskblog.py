from flask import Flask
app = Flask( __name__ )

@app.route("/home") # this is a route , decorator 
def hello(): 
    return "<h1>Hello World!</h1>"

@app.route("/about") # this is a route , decorator 
def about(): 
    return "<h1>About</h1>"

if __name__ == '__main__':
    app.run( debug = True )

