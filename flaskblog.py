from flask import Flask
app = Flask( __name__ )

@app.route("/") # this is a route , decorator 
def hello(): 
    return "Hello World!"


