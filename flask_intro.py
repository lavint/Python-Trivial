''' Use Flask to develop APIs and distribute data from a server which listens requests in particular endpoints (Urls)'''

from flask import Flask
from sqlalchemy import create_engine
import os
import jsonify


app = Flask(__name__)
# os.chdir('Lav_GitHub\Python-Trivial')
print(os.getcwd())
database_path = 'Resources/geo.sqlite'
engine = create_engine(f'sqlite:///{database_path}')
geo_data = engine.execute('SELECT * FROM COUNTRY')
# geo_data

# @app.route() is a function decorator which takes the route's URL as its argument
# Routes must return HTTP responses
# Use jsonify library to create an HTTP response with the dictionary to send back to the client
# Flask 1.1.0 +  automatically convert dictionary to JSON
# Endpoint starts with /api to indicate to consumers that the response will contain data


# Define a function that describe the server's response when a user hits the index route
@app.route("/")
def index():
    
    # Server executes the request
    print('Server received request for Home page')
    
    # Client receives request handler (function)'s return value
    return 'Welcome to the app!!'


@app.route("/about")
def about():
    print('Server received request for About Page')
    return 'Learn about about us!'


# @app.route("/api/v1.0/geography")
# def geo():
#     return jsonify(geo_data)



if __name__ == "__main__":
    app.run(debug=True)   # set debug to False in production
