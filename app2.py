# Import the dependencies
import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

# Flask Setup
app = Flask(__name__)

measurements_df = pd.read_csv("https://raw.githubusercontent.com/greenboi105/Flask-Surf-Weather-Station-API/main/Resources/hawaii_measurements.csv")
measurements_df['date'] = pd.to_datetime(measurements_df['date'])

stations_df = pd.read_csv("https://raw.githubusercontent.com/greenboi105/Flask-Surf-Weather-Station-API/main/Resources/hawaii_stations.csv")


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
    begin_date = pd.to_datetime(dt.date(2017, 8, 23) - dt.timedelta(days=365))

    # Selects the "date" and "prcp" columns from the "Measurement" table and filter the data 
    filtered_data = measurements_df[measurements_df['date'] >= begin_date].sort_values('date')[['date', 'prcp']]

    # Create a dictionary where the date is the key and the precipitation is the value 
    precipitation = [{str(date): prcp} for date, prcp in zip(list(filtered_data['date']), list(filtered_data['prcp']))]

    return jsonify(precipitation)


@app.route('/api/v1.0/stations')
def stations():

    # Query station data
    results = stations_df.copy()

    # Create a list of dictionaries representing stations
    station_data = [
        {
        "Station": station, 
        "Name": name,
        "Latitude": latitude,
        "Longitude": longitude,
        "Elevation": elevation
        } 
    for station, name, latitude, longitude, elevation in zip(list(results['station']), list(results['name']), list(results['latitude']), list(results['longitude']), list(results['elevation']))]

    return jsonify(station_data)


@app.route('/api/v1.0/tobs')
def tobs():

    # Find the most-active station
    most_active_station = measurements_df.groupby('station').size().reset_index(name='count').sort_values('count', ascending=False).head(1)
    
    # Get the most-active station
    most_active_station_id = most_active_station['station'].iloc[0]

    # Calculate the date one year ago from the last date
    one_year_ago = pd.to_datetime(dt.date(2017, 8, 23) - dt.timedelta(days=365))

    # Query temperature observations for the most-active station
    results = measurements_df[(measurements_df['station'] == most_active_station_id) & 
                                (measurements_df['date'] >= one_year_ago)][['date', 'tobs']]

    # Create a list of dictionaries representing temperature observations
    tobs_data = [
        {
        "Date": str(date),
        "Temperature": tobs,
        "Most Active Station": most_active_station_id
        } 
    for date, tobs in zip(list(results['date']), list(results['tobs']))]

    return jsonify(tobs_data)


@app.route("/api/v1.0/temp/<start>")
def start_stats(start=None):

    # Filter the DataFrame based on the start date
    filtered_df = measurements_df[measurements_df['date'] >= start]

    # Calculate min, max, and avg of 'tobs'
    min_tobs = filtered_df['tobs'].min()
    max_tobs = filtered_df['tobs'].max()
    avg_tobs = filtered_df['tobs'].mean()

    temp_stats = [
        {
            'Minimum Temp' : min_tobs, 
            'Maximum Temp' : max_tobs,
            'Average Temp': avg_tobs
        } 
    ]

    return jsonify(temp_stats)

@app.route('/api/v1.0/temp/<start>/<end>')
def calc_stats(start, end):

    # Query the database to calculate TMIN, TAVG, and TMAX for the specified date range
    filtered_df = measurements_df[(measurements_df['date'] >= start) & (measurements_df['date'] <= end)]
    results = list(filtered_df['tobs'].agg(['min', 'mean', 'max']))

    # Create a dictionary from the row data and append to a list of for the temperature data
    temp_stats = [
        {
            'Minimum Temp' : results[0], 
            'Maximum Temp' : results[1],
            'Average Temp': results[2]
        } 
    ]

    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)
    