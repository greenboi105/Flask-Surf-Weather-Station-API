# Import the dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

from path import file_path

# Database Setup - connect to database and import existing tables
engine = create_engine(f"sqlite:///{file_path}")
Base = automap_base()
Base.prepare(autoload_with=engine)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create session
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def homepage():

    """List all available API routes."""
    return (
        "<b>SURFSUP!! THE CLIMATE APP API</b><br/><br/>"
        "Available Routes:<br/><br/>"
        "<b>Precipitation Data</b><br/>"
        "/api/v1.0/precipitation<br/><br/>"
        "<b>List of Stations</b><br/>"
        "/api/v1.0/stations<br/><br/>"
        "<b>Temperature Data of the Most Active Station</b><br/>"
        "/api/v1.0/tobs<br/><br/>"
        "<b>Temperature Data on Specific Date</b><br/>"
        "/api/v1.0/temp/YYYY-MM-DD<br/>"
        "/api/v1.0/temp/YYYY-MM-DD(Start)/YYYY-MM-DD(End)"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():

    # Calculate the year prior to the last date
    begin_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Selects the "date" and "prcp" columns from the "Measurement" table and filter the data 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= begin_date).order_by(Measurement.date).all()

    # Create a dictionary where the date is the key and the precipitation is the value 
    precipitation = [{date: prcp} for date, prcp in results]

    session.close()

    return jsonify(precipitation)


@app.route('/api/v1.0/stations')
def stations():

    # Query station data
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a list of dictionaries representing stations
    station_data = [
        {
        "Station": station, 
        "Name": name,
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation": elevation
        } 
    for station, name, latitude, longitude, elevation in results]

    session.close()

    return jsonify(station_data)


@app.route('/api/v1.0/tobs')
def tobs():

    # Find the most-active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    # Get the most-active station
    most_active_station_id = most_active_station[0]

    # Calculate the date one year ago from the last date
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query temperature observations for the most-active station
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= one_year_ago).all()

    # Create a list of dictionaries representing temperature observations
    tobs_data = [
        {
        "Date": date,
        "Temperature": tobs,
        "Most Active Station": most_active_station_id
        } 
    for date, tobs in results]

    session.close()

    return jsonify(tobs_data)


@app.route("/api/v1.0/temp/<start>")
def start_stats(start=None):

    # Query the database to calculate TMIN, TAVG, and TMAX for the specified date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of for the temperature data
    temp_stats = [
        {
            'Minimum Temp' : Tmin, 
            'Maximum Temp' : Tmax,
            'Average Temp': Tavg
        } 
        for Tmin, Tmax, Tavg in results
    ]

    session.close()

    return jsonify(temp_stats)


@app.route('/api/v1.0/temp/<start>/<end>')
def calc_stats(start, end):

    # Query the database to calculate TMIN, TAVG, and TMAX for the specified date range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of for the temperature data
    temp_stats = [
        {
            'Minimum Temp' : Tmin, 
            'Maximum Temp' : Tmax,
            'Average Temp': Tavg
        } 
        for Tmin, Tmax, Tavg in results
    ]
    
    session.close()

    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)