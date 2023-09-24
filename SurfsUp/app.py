# Import the dependencies.
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Create a dictionary of routes and their descriptions
routes_dic = {
    "/api/v1.0/precipitation": "Convert the query results to a dictionary by using date as the key and prcp as the value.",
    "/api/v1.0/stations": "Return a JSON list of stations from the dataset.",
    "/api/v1.0/tobs":"Return a JSON list of stations from the dataset",
    "/api/v1.0/<start>": "Query temperature data for a specified start date.",
    "/api/v1.0/<start>/<end>": "Query temperature data for a specified date range.",
}
# 3. Define static routes
@app.route("/")
def homepage():
    return routes_dic

# Define a route for /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Get the description for the /api/v1.0/precipitation route
    description = routes_dic["/api/v1.0/precipitation"]
    return description

# 4. Define main behaviour
if __name__ == "__main__":
    app.run(debug=True)

