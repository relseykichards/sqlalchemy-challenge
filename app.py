# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
Base.metadata.create_all(engine)
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
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
    # List all available API routes
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

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    precip_twelve_months = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_twelve_months.append(precip_dict)

    return jsonify(precip_twelve_months)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB 
    session = Session(engine)

    # Return a list of all station names
    results = session.query(Measurement.station).distinct(Measurement.station).all()
    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB and query results
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    temp_twelve_months = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_twelve_months.append(temp_dict)

    return jsonify(temp_twelve_months)

@app.route("/api/v1.0/<start>")
def start_date(start):

# establish date input and format
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year

# Create our session (link) from Python to the DB and query results
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    starting_date = list(np.ravel(results))
    return jsonify(starting_date)

    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    # establish date input and format
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year

    # Create our session (link) from Python to the DB and query results
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    starting_ending = list(np.ravel(result))
    return jsonify(starting_ending)


if __name__ == '__main__':
    app.run(debug=True)