# Import the dependencies.
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
station=base.classes.station
measurement=base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )





@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all precipitation data"""
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-24").all
    
    session.close()
    
    # Convert list into dictionary
    prcp_all = []
    for date, prcp in results:
        prcp_dict={}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        prcp_all.append(prcp_dict)
        
    return jsonify(prcp_all)





@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all stations"""
    # Query all stations
    results = session.query(station.station).order_by(station.station).all()
    
    session.close()
    
    # Convert list of tuples into normal list
    stations_all = list(np.ravel(results))
    
    return jsonify(stations_all)





@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all tobs"""
    # Query all tobs
    results = session.query(measurement.date, measurement.tobs).\
                filter(measurement.date >= '2016-08-24').\
                filter(measurement.station=='USC00519281').\
                order_by(measurement.date).all()
    
    session.close()
    
    # Convert list of tuples into dictionary
    tobs_all = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        tobs_all.append(tobs_dict)
    
    return jsonify(tobs_all)





@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all min, average, and max tobs for a given start date"""
    # Query all tobs
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    session.close()
    
    # Create dictionary from row data and append to list of start_tobs
    start_tobs = []
    for min, avg, max in results:
        start_tobs_dict = {}
        start_tobs_dict["tmin"] = min
        start_tobs_dict["tavg"] = avg
        start_tobs_dict["tmax"] = max
        start_tobs.append(start_tobs_dict)
        
    return jsonify(start_tobs)





@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all min, average, and max tobs for a given start and end date range"""
    # Query all tobs
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    
    # Create dictionary from row data and append to list of start_end_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["tmin"] = min
        start_end_tobs_dict["tavg"] = avg
        start_end_tobs_dict["tmax"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_end_tobs)





if __name__ == "__main__":
    app.run(debug=True)
