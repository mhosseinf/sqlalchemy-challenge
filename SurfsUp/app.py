# Import the dependencies.
from flask import Flask, jsonify, request
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
    "/api/v1.0/precipitation": "Return a JSON list of precipitation data.",
    "/api/v1.0/stations": "Return a JSON list of weather stations in the dataset.",
    "/api/v1.0/tobs": "Return a JSON list of temperature observations for the last year from the most active weather station.",
    "/api/v1.0/<start>": "Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.",
    "/api/v1.0/<start>/<end>": "Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified date range.",
}


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

   # Query to list all precipitation based on date as the key and prcp value and convert the results to a dictionary 
    # Query to get precipitation data
    results2 = session.query(Measurement.date, Measurement.prcp).all()
    
    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results2}
    
    # Close the session to release resources
    session.close()
    return jsonify(precipitation_data)


# 3.Define a route for /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
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
    
    # Query to get a list of stations
    results3 = session.query(Station.station, Station.name).all()
    
    # Create a list of stations and their names
    station_list = [{"station": station, "name": name} for station, name in results3]
    # Close the session to release resources
    session.close()
    return jsonify(station_list)


# 4.Define a route for /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
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
    
    # Find the most active station from the previous query    
    most_active_station = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the most recent date in the database
    most_recent_date = session.query(Measurement.date).\
    filter(Measurement.station == most_active_station).\
    order_by(Measurement.date.desc()).first()[0]
    one_year_ago = (dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)).date()

    # Query the temperature observations (TOBS) data for the most active station for the last 12 months
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= one_year_ago).all()

    # Create a list of temperature observations
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    # Close the session to release resources
    session.close()
    return jsonify(tobs_list)

# 5.Define a route for /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def Specified_date_range(start, end):
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
    Measurement = Base.classes.measurement
    
    # Convert the user input into datetime objects 
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # Check if the end date is before the start date
    if end_date < start_date:
        return jsonify({"error": "End date cannot be before the start date."})
    
    # calculate the lowest, highest, and average temperature for the specified dates
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date.between(start_date, end_date)).all()

    # Extract the temperature statistics values
    min_temp, max_temp, avg_temp = temperature_stats[0]

    # Create a dictionary to store the temperature statistics
    temperature_dict = {
    "start_date": start_date,
    "End_date": end_date,
    "min_temperature": min_temp,
    "max_temperature": max_temp,
    "avg_temperature": avg_temp
    }
    # Close the session to release resources
    session.close()
    return jsonify(temperature_dict)



# 1. Define main behaviour
if __name__ == "__main__":
    app.run(debug=True)

