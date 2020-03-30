
# coding: utf-8


import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
inspector = inspect(engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Welcome():
    
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"//api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date
    last_year = str(int(latest_date[:4])-1) + latest_date[4:]


    query_date = last_year
    lastYearPrec = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>query_date).all()
    #print((lastYearPrec))


    lastYearPrecipitation= []
    for result in lastYearPrec:
        line = {}
        line["date"] = result[0]
        line["prcp"] = result[1]
        lastYearPrecipitation.append(line)

    return jsonify(lastYearprecipitation)




@app.route("/api/v1.0/stations")
def stations():


    # What are the most active stations? (i.e. what stations have the most rows)?
    # List the stations and the counts in descending order.
    stationsList = session.query(Measurement.station).all()

    return jsonify(stationsList)


@app.route("/api/v1.0/tobs")
def tobs():
    last12TOBS = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station =='USC00519281', Measurement.date>query_date).all()
    
    last12TOBS_list=[]
    for tobs in last12TOBS:
        tobsdict = {}
        tobsdict["station"] = tobs[0]
        tobsdict["tobs"] = tobs[1]
       
        last12TOBS_list.append(tobsdict)
    return jsonify(last12TOBS_list)

    




if __name__ == '__main__':
    app.run(debug=True)