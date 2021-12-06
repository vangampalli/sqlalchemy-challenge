from flask import Flask, jsonify 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)
Measurement = Base.classes.measurement
Station = Base.classes.station 

app = Flask(__name__)

@app.route("/")
def welcome():

    return (
        f"Welcome to the Weather Stations API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation(): 
    session = Session(engine)
    dates = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>='2016-08-23').all()
    prcp_dict = {}
    for date, prcp in dates: 
        prcp_dict[date] = prcp 
    return jsonify(prcp_dict)
    session.close()

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    stations = session.query(Station.name, Station.station).all()
    prcp_dict = {}
    for name, station in stations: 
        prcp_dict[name] = station 
    return jsonify(prcp_dict)
    session.close()

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by('station').\
    order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0]
    most_tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == most_active[0]).all()
    temps = []
    for tob in most_tobs: 
        (temp) = tob
        temps.append(temp.tobs)
    return jsonify(temps)
    session.close()

@app.route('/api/v1.0/<start>')
def temp_start(start):
    session = Session(engine)
    most_tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= start).all()
    
    temps = []
    for tob in most_tobs: 
        (temp) = tob
        temps.append(temp.tobs)
    temps_dict = {}
    temps_dict["TMIN"] = min(temps)
    temps_dict["TMAX"] = max(temps)
    temps_dict["TAVG"] = sum(temps)/len(temps)
    return jsonify(temps_dict)
    session.close()

@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    session = Session(engine)
    most_tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    temps = []
    for tob in most_tobs: 
        (temp) = tob
        temps.append(temp.tobs)
    temps_dict = {}
    temps_dict["TMIN"] = min(temps)
    temps_dict["TMAX"] = max(temps)
    temps_dict["TAVG"] = sum(temps)/len(temps)
    return jsonify(temps_dict)
    session.close()

if __name__ == "__main__":
    app.run(debug=True)
