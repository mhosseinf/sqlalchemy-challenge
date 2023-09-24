# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt
from sqlalchemy.ext.automap import automap_base


#Create an app, being sure to pass __name__
#################################################
# Flask Setup
################################################# 
app = Flask(__name__)

# Create a dictionary of routes and their descriptions
routes_dic = {
    "/api/v1.0/precipitation": "Convert the query results to a dictionary by using date as the key and prcp as the value.",
    "/api/v1.0/stations": "Return a JSON list of stations from the dataset.",
    "/api/v1.0/tobs":"Return a JSON list of stations from the dataset",
    "/api/v1.0/<start>": "Query temperature data for a specified start date.",
    "/api/v1.0/<start>/<end>": "Query temperature data for a specified date range.",
}
# Create an SQLAlchemy engine and session to interact with your database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Routes
#################################################
# 1. Define static routes
@app.route("/")
def homepage():
    return routes_dic

# 2.Define a route for /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the most recent date in the database
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query to get precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


# 1. Define main behaviour
if __name__ == "__main__":
    app.run(debug=True)

