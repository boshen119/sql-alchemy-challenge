#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Datavase Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session link from Python to DB
session = Session(engine)

# Flask setup
app = Flask(__name__)

#Flask Routes endpoints
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API! <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Return the precipitation data from last year
    prev_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).        filter(Measurement.date >= prev_year).all()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

if __name__ == '__main__':
    app.run()

