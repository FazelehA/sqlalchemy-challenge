import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/Temperature Observation Data for last 12 months<br/>"
        f"Temperature Stats starting from: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature Stats starting from/ending at: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

#################################################
# Precipitation Route
#################################################

@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()

     # Create a dictionary as date the key and prcp as the value
    precipitation = []
    for result in query:
        dictionary = {}
        dictionary["date"]=result[0]
        dictionary["prcp"]=result[1]
        precipitation.append(dictionary)

    return jsonify(precipitation )

#################################################
# Station Route
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create the session link
    session = Session(engine)
    
    # Query data to get stations list
    query = session.query(Station.station, Station.name).all()
    
    session.close()

    # Return Json list of stations from the dataset
    station_list = []
    for result in query:
        dictionary = {}
        dictionary["station"]= result[0]
        dictionary["name"] = result[1]
        station_list.append(dictionary)
    
    # jsonify the list
    return jsonify(station_list)

#################################################
# TOBS Route
#################################################

@app.route("/api/v1.0/Temperature Observation Data for last 12 months")
def tobs():
    # create session link
    session = Session(engine)
    
    # Query data to get tobs
    query = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= "2016-08-23").all()

    session.close()

    # convert list of tuples to show date and temprature values
    tobs_list = []
    for result in query:
        dictionary = {}
        dictionary["date"] = result[1]
        dictionary["temprature"] = result[0]
        tobs_list.append(dictionary)

    # jsonify the list
    return jsonify(tobs_list)

#################################################
#Temp Stats Start Date Route
#################################################

@app.route("/api/v1.0/<start>")
def stats(start):
    # create session link
    session = Session(engine)
    
    # convert date to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # query data for the start date value
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Create a list to hold results
    temp_stats = []
    for result in query:
        dictionary = {}
        dictionary["StartDate"] = start_date
        dictionary["TMIN"] = result[0]
        dictionary["TAVG"] = result[1]
        dictionary["TMAX"] = result[2]
        temp_stats.append(dictionary)

    # jsonify the result
    return jsonify(temp_stats)

#################################################
#Temp Stats Start/end Date Route
#################################################

@app.route("/api/v1.0/<start>/<stop>)")
def temp_stats_2(start, stop):
    # create session link
    session = Session(engine)

    # convert dates to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(stop, "%Y-%m-%d")

    # query data for the start date value
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)

    session.close()

    # Create a list to hold results
    temp_stats_2 = []
    for result in query:
        dictionary = {}
        dictionary["StartDate"] = start_date
        dictionary["EndDate"] = end_date
        dictionary["TMIN"] = result[0]
        dictionary["TAVG"] = result[1]
        dictionary["TMAX"] = result[2]
        temp_stats_2.append(dictionary)

    # jsonify the result
    return jsonify(temp_stats_2)
    
if __name__ == "__main__":
    app.run(debug=True)