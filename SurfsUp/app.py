# Import the dependencies.
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

# Save references to each table
Base.classes.keys()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Base.classes.keys()
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_date = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date > one_year).\
        order_by(Measurement.date).all()
    
    session.close()

    all_prcp = []
    for a in precipitation_date:
        row = {}
        row["date"] = precipitation_date[0]
        row["prcp"] = precipitation_date[1]
        all_prcp.append(row)

        total_prcp = list(np.ravel(precipitation_date))
    
    return jsonify(total_prcp)

    # result = {date:prcp for date,prcp in precipitation_date}    

    # for i in result:
    #     print (i)
    # return jsonify(result)

@app.route("/api/v1.0/stations")
def stations():
    
   # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    past_year = dt.date(2017, 8, 18) - dt.timedelta(days=365) 
    temp_data = session.query(Measurement.tobs).\
        filter(Measurement.date >= past_year).filter(Measurement.station =='USC00519281').\
        order_by(Measurement.tobs).all()
    
    session.close()
    
    #Return a JSON list of temperature observations for the previous year.
    #all_temperatures = []
    for date in temp_data:
        # tobs_dict={}
        # tobs_dict['date'] = date
        # tobs_dict['tobs'] = tobs
        # all_temperatures.append(tobs_dict)
        print(temp_data)
    
    tobs_data = list(np.ravel(temp_data))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    
    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    
    date_input = dt.datetime.strptime(start, "%m%d%Y")
    
    min_avg_max = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date >= date_input).all()
    
    session.close()
 
    min_list = list(np.ravel(min_avg_max))

    return jsonify(min_list)
    


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    date_input = dt.datetime.strptime(start, "%m%d%Y")
    end_input = dt.datetime.strptime(end, "%m%d%Y")
    last = dt.timedelta(days=365)
    start = date_input - last
    end = end_input - last

    min_avg_max2 = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurements.date <= end).all()

    session.close()

    ranges = list(np.ravel(min_avg_max2))

    return jsonify(ranges)

if __name__ =="__main__":
    app.run(debug = True)
