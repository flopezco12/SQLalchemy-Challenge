# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt

from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of precipitation and date"""
    # Query all precipitaion and date
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of precipitation and date"""
    # Query all stations' names, ids, coordinates, and altitude
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = []
    for id, station, name, latitude, longitude, elevation in results:
        stations_dict = {}
        stations_dict["Id"] = id
        stations_dict["Station"] = station
        stations_dict["Name"] = name
        stations_dict["Latitude"] = latitude
        stations_dict["Longitude"] = longitude
        stations_dict["Elevation"] = elevation
        all_stations.append(stations_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of temperature and date"""
    # Query all temperature records
    Most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(Most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).filter(Measurement.date >= last_year).all()
    session.close()

    # Convert list of tuples into normal list
    all_temp = []
    for tobs, date in results:
        temp_dict = {}
        temp_dict["temp"] = tobs
        temp_dict["date"] = date
        all_temp.append(temp_dict)

    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates."""

    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temps={}
    temps["min_Temp"]=results[0][0]
    temps["avg_Temp"]=results[0][1]
    temps["max_Temp"]=results[0][2]

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)












































