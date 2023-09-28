# sqlalchemy-challenge
Module 10 Challenge

This repository contains a comprehensive climate analysis toolkit for a fictional location in Hawaii. It utilises Python, SQLAlchemy, Pandas, and Matplotlib to analyse and visualise weather data from a SQLite database. 

Flask API
In addition to the SQLAlchemy-based analysis, this repository also contains a Flask-based API that provides climate analysis data from the weather dataset. Please note that the API leverages SQLAlchemy to interact with a SQLite database containing weather data. It's designed to provide insights and statistics on climate data for analysis and research purposes.


1-The Jupyter code is organised into two parts:

Code Overview:
Database Setup: The code establishes a connection to the SQLite database containing weather data from multiple stations in Hawaii using the creating engine, base, and session. Also, assign two classes, Station and Measurement, to variables.

Precipitation Analysis and Plotting: 
It identifies the latest date in the dataset, retrieves and analyses the precipitation data for the preceding 12 months, and then visualises the results in a bar chart using Matplotlib. Additionally, summary statistics are provided for the precipitation data.

Station Analysis: 
The code calculates the total number of weather stations and identifies the most active station based on the number of data points.

Temperature Analysis: It retrieves and analyses temperature observation data (TOBS) for the most active station over the last 12 months. The results are plotted as a histogram.

Technologies Used:
Python
SQLAlchemy
Pandas
Matplotlib



2-The API offers the following routes:

2-1-Precipitation: /api/v1.0/precipitation
Returns a JSON list of precipitation data.


2-2-Stations: /api/v1.0/stations
Returns a JSON list of weather stations in the dataset.


2-3-Temperature Observations (TOBS): /api/v1.0/tobs
Returns a JSON list of temperature observations from the most active weather station for the last year.


2-4-Temperature Statistics by Date Range: /api/v1.0/<start>/<end>
Returns a JSON list of the minimum, average, and maximum temperatures for a specified date range.
ie, http://127.0.0.1:5000/api/v1.0/2016-01-01/2017-12-31


2-5-Temperature Statistics by Start Date: /api/v1.0/<start>
Returns a JSON list of the minimum, average, and maximum temperatures for a period between a specified start date and the most recent date in the dataset
ie, http://127.0.0.1:5000/api/v1.0/2016-01-01






