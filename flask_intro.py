''' Use Flask to develop APIs and distribute data from a server which listens requests in particular endpoints (Urls)'''

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import os
import numpy as np



app = Flask(__name__)

database_path = 'Resources/geo.sqlite'
engine = create_engine(f'sqlite:///{database_path}')
Base = automap_base()
Base.prepare(engine, reflect=True)
Continent = Base.classes.continent


# @app.route() is a function decorator which takes the route's URL as its argument
# Routes must return HTTP responses (need dictionart or LIST of dictionaries as input)
# Use jsonify library to create an HTTP response with the dictionary to send back to the client
# Flask 1.1.0 +  automatically convert a dictionary to JSON
# Endpoint starts with /api to indicate to consumers that the response will contain data
# Add trailing / in route to avoid 404 error when accessing with / and parameter as in country and country_spec below

# Define a function that describe the server's response when a user hits the index route
@app.route("/")
def index():
    
    # Server executes the request
    print('Server received request for Home page')
    
    # Client receives request handler (function)'s return value
    return ('Welcome to the app!!<br>'
            'Available routes:</br>'
            '/about<br>'
            '/api/v1.0/continent<br>'
            '/api/v1.0/country<br>'
            '/api/v1.0/country/Insert_Country_Name_Here'
    )



@app.route("/about/")
def about():
    print('Server received request for About Page')
    return 'Learn about about us :)!'


# Pull data using session
@app.route("/api/v1.0/continent/")
def continent(): 
    session = Session(engine)   
    all_continents = session.query(Continent.name).all()
    session.close()
    
    # Convert a list of tuples to list, then to json and return result
    return jsonify(list(np.ravel(all_continents)))
        

# Pull data using engine.execute
@app.route("/api/v1.0/country/")
def country():
    all_countries = []
    for index, country, capital in engine.execute("SELECT * FROM COUNTRY"):
        countries_dict = {}
        countries_dict['country'] = country
        countries_dict['capital'] = capital
        all_countries.append(countries_dict)
        
    # Convert a list to json and return result
    return jsonify(all_countries)



# Search for specific country in the URL
# Canonicalization is a process for converting data that has more than one possible representation into a standard form
@app.route("/api/v1.0/country/<country>/") 
def country_spec(country):
    for index, cntry, capital in engine.execute("SELECT * FROM COUNTRY"):
        if cntry.lower() == country.lower():
            return jsonify({cntry: capital})     

    # Return error message
    return jsonify({'Error': f'Country {country} not found'}), 404



if __name__ == "__main__":
#     app.run(debug=True)   # NOT working with sqlalchemy # set debug to False in production 
    app.run(port=5000)
