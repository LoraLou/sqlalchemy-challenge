
# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd 
import datetime as dt
import numpy as np 
#Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#################################################
# Database Setup
#################################################
engine = create_engine(("sqlite:///Resources/hawaii.sqlite"))
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
# create an app
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
#Home route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather API<br/>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/temperature<br>"
        f"For Start: /api/v1.0/<start><br>"
        f"For Start/End: /api/v1.0/<start>/<end><br>"
        f"note: date must be YYYYMMDD format"
    )
#precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation_output():
    year_ago_date = dt.datetime(2017,8,23) - dt.timedelta(days=365)
    precipitation_value = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago_date).all()
    session.close()
    precipitation_amount = {date: precipitation for date, precipitation in precipitation_value}
    return jsonify(precipitation_amount)

#station route 
@app.route("/api/v1.0/stations")
def station_output():
    every_station = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(every_station))
    return jsonify(all_stations)

#temperature route 
@app.route("/api/v1.0/temperature")
def temperature_output():
     year_ago_date = dt.datetime(2017,8,23) - dt.timedelta(days=365)
     most_active_station_12month_temperature = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago_date).all()
     session.close()
     temperature_value = list(np.ravel(most_active_station_12month_temperature))
     return jsonify(temperatures = temperature_value)

#start and end
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        session.close()
        temperatures = list(np.ravel(results))
        return jsonify(temperatures=temperatures)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures=temperatures)


if __name__ == '__main__':
     app.run()
