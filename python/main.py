from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import searchForm
import secrets
from collections import defaultdict

from api_caller import get_stations_by_coordinates, load_all_stations, get_weather_data_of_station_by_station_id

secret_key = secrets.token_urlsafe(16)


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secret_key

#Initialization
app.allStations = load_all_stations()

class SearchData:
    def __init__(self,latitude,longitude,radius,startYear,endYear,stationCount):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.startYear = startYear
        self.endYear = endYear
        self.stationCount = stationCount

    #TODO: in klasse lassen? oder direkt aufruden?
    def getStations(latitude, longitude, radius, stationCount):
        print("Stationen werden ermittelt...")
        return get_stations_by_coordinates(app.allStations,latitude, longitude, radius, stationCount)

def update_session_form(form):
    #Update Session (Form)
    session['latitude'] = form.latitude.data
    session['longitude'] = form.longitude.data
    session['radius'] = form.radius.data
    session['stationCount'] = form.stationCount.data
    session['startYear'] = form.startYear.data #Keine Anforderung
    session['endYear'] = form.endYear.data #Keine Anforderung

def fill_form():
    form = searchForm(request.form)
    form.latitude.data = float(session['latitude'])
    form.longitude.data = float(session['longitude'])
    form.radius.data = session['radius']
    form.stationCount.data = session['stationCount']
    form.startYear.data = session['startYear']
    form.endYear.data = session['endYear']
    return form


@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        update_session_form(form)
        # formData = SearchData(form.latitude.data,form.longitude.data,form.radius.data,form.startYear.data, form.endYear.data,form.stationCount.data)    
        session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
        return redirect(url_for('list'))   
    
    #Beim ersten mal aufrufen der App
    if(session.get('latitude') is not None):
        form.latitude.data = float(session['latitude'])
        form.longitude.data = float(session['longitude'])
        form.radius.data = session['radius']
        form.stationCount.data = session['stationCount']
        form.startYear.data = session['startYear'] #Keine Anforderung
        form.endYear.data = session['endYear'] #Keine Anforderung
    else:
        #Standort Fürth
        form.latitude.data = 49.4771
        form.longitude.data = 10.9887

        #Standard-Werte
        form.radius.data = 50
        form.stationCount.data = 5
        form.startYear.data = 1949 #Keine Anforderung
        form.endYear.data = 2024 #Keine Anforderung
    return render_template('Startseite.html', form=form)

@app.route("/jahresansicht/<id>")
def yearView(id):
    form = searchForm(request.form)
    
    if request.method == 'GET':

        #! Folgendes nicht löschen
        
        # stationTemperatures = get_weather_data_of_station_by_station_id(id, session['startYear'], session['endYear'])
        # stationTemperatures = dict(stationTemperatures)

        # if not stationTemperatures:
        #     flash('Der ausgewählte Zeitraum enthält keine Daten')
        # else:
        #     session['stationWeatherData'] = stationTemperatures
        #     #Mittelwerte berechnen
                            
        #     averageTemperaturesYear = defaultdict(lambda: dict())
        #     #Test Mittelwert Jahr
        #     for year in stationTemperatures:
        #         divisor = 0
        #         sumMin = 0
        #         sumMax = 0
        #         for month in stationTemperatures[year]:
        #             for day in stationTemperatures[year][month]:
        #                 divisor += 1
        #                 sumMin += stationTemperatures[year][month][day]['TMIN']
        #                 sumMax += stationTemperatures[year][month][day]['TMAX']
        #         averageTemperaturesYear[year]['TMIN'] = round(sumMin/divisor,1)
        #         averageTemperaturesYear[year]['TMAX'] = round(sumMax/divisor,1)
    
    
        #TESTDATEN
        averageTemperaturesYear = {
                        1949: {'TMIN': 4.3, 'TMAX': 14.7},
                        1950: {'TMIN': 5.1, 'TMAX': 15.2},
                        1951: {'TMIN': 3.8, 'TMAX': 14.5},
                        1952: {'TMIN': 6.2, 'TMAX': 16.8},
                        1953: {'TMIN': 4.5, 'TMAX': 15.0},
                        1954: {'TMIN': 5.3, 'TMAX': 15.7},
                        1955: {'TMIN': 4.8, 'TMAX': 14.9},
                        1956: {'TMIN': 6.0, 'TMAX': 16.5},
                        1957: {'TMIN': 5.7, 'TMAX': 15.4},
                        1958: {'TMIN': 4.1, 'TMAX': 14.2},
                        1959: {'TMIN': 5.6, 'TMAX': 15.8},
                        1960: {'TMIN': 4.9, 'TMAX': 15.1},
                        1961: {'TMIN': 5.2, 'TMAX': 15.3},
                        1962: {'TMIN': 4.4, 'TMAX': 14.6},
                        1963: {'TMIN': 5.0, 'TMAX': 15.6},
                        1964: {'TMIN': 6.1, 'TMAX': 16.2},
                        1965: {'TMIN': 4.7, 'TMAX': 15.5},
                        1966: {'TMIN': 5.4, 'TMAX': 15.9},
                        1967: {'TMIN': 4.2, 'TMAX': 14.3},
                        1969: {'TMIN': 5.5, 'TMAX': 16.0},
                        1970: {'TMIN': 5.5, 'TMAX': 16.0},
                        1971: {'TMIN': 5.5, 'TMAX': 16.0},
                        1972: {'TMIN': 5.5, 'TMAX': 16.0},
                        1973: {'TMIN': 5.5, 'TMAX': 16.0},
                        1974: {'TMIN': 5.5, 'TMAX': 16.0},
                        1975: {'TMIN': 5.5, 'TMAX': 16.0},
                        1976: {'TMIN': 5.5, 'TMAX': 16.0},
                        1977: {'TMIN': 5.5, 'TMAX': 16.0},
                        1978: {'TMIN': 5.5, 'TMAX': 16.0},
                        # Füge hier weitere Jahre mit den entsprechenden Temperaturwerten hinzu
                    }

    return render_template('Jahresansicht.html',form=form, averageTemperaturesYear = averageTemperaturesYear, id=id)

@app.route("/liste", methods=['POST', 'GET'])
def list():
    
    if(session.get('latitude') is not None):
        form = fill_form()
    else:
        form = searchForm(request.form)
            # form.latitude.data = session['latitude']
            # form.longitude.data = session['longitude']
            # form.radius.data = session['radius']
            # form.stationCount.data = session['stationCount']
            # form.startYear.data = session['startYear'] #Keine Anforderung
            # form.endYear.data = session['endYear'] #Keine Anforderung

    if request.method == 'POST' and form.validate_on_submit():
        # formData = SearchData(form.latitude.data,form.longitude.data,form.radius.data,form.startYear.data, form.endYear.data,form.stationCount.data)    
        session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
        
        #Update Session (Form)
        update_session_form(form)
        # session['latitude'] = formData.latitude
        # session['longitude'] = formData.longitude
        # session['radius'] = formData.radius
        # session['stationCount'] = formData.stationCount
        # session['startYear'] = formData.startYear #Keine Anforderung
        # session['endYear'] = formData.endYear #Keine Anforderung
        return redirect(url_for('list'))
    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)

            # form.latitude.data = float(session['latitude'])
            # form.longitude.data = float(session['longitude'])
            # form.radius.data = session['radius']
            # form.stationCount.data = session['stationCount']
            # form.startYear.data = session['startYear'] #Keine Anforderung
            # form.endYear.data = session['endYear'] #Keine Anforderung

    return render_template('Liste.html',form=form, stations=session['userStations'])

@app.route("/monatsansicht")
def monthView():
    form = searchForm(request.form)
    return render_template('Monatsansicht.html', form=form)

#! Es gibt keine Tagesansicht?
# @app.route("/tagesansicht")
# def dayView():
#     form = searchForm(request.form)
#     return render_template('Tagesansicht.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)