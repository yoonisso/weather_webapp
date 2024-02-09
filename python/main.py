from flask import Flask, render_template, request, flash, redirect, url_for, session, Response
from forms import searchForm, seasonsForm
import secrets
from datetime import date
from bokeh.plotting import figure
from bokeh.embed import components
from helpers.diagram_ploter import DiagramPloter
from collections import defaultdict

from api_caller import get_stations_by_coordinates, load_all_stations, get_weather_data_of_station_by_station_id

secret_key = secrets.token_urlsafe(16)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secret_key

#Initialization
app.allStations = load_all_stations()
app.stationTemperatures = {}


class SearchData:
    def __init__(self,latitude,longitude,radius,start_year,end_year,station_count):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.startYear = start_year
        self.endYear = end_year
        self.stationCount = station_count

    #TODO: in klasse lassen? oder direkt aufruden?
    def getStations(latitude, longitude, radius, stationCount):
        print("Stationen werden ermittelt...")
        return get_stations_by_coordinates(app.allStations,latitude, longitude, radius, stationCount)

def update_session_form(form):
    #Update Session (Form)
    session['latitude'] = form.latitude.data
    session['longitude'] = form.longitude.data
    session['radius'] = form.radius.data
    session['station_count'] = form.station_count.data
    session['start_year'] = form.start_year.data #Keine Anforderung
    session['end_year'] = form.end_year.data #Keine Anforderung

def fill_form():
    form = searchForm(request.form)
    form.latitude.data = float(session['latitude'])
    form.longitude.data = float(session['longitude'])
    form.radius.data = session['radius']
    form.station_count.data = session['station_count']
    form.start_year.data = session['start_year']
    form.end_year.data = session['end_year']
    return form

def update_seasons_form(seasonsForm):
    session['year_tmin'] = seasonsForm.year_tmin.data
    session['year_tmax'] = seasonsForm.year_tmax.data
    session['spring_tmin'] = seasonsForm.spring_tmin.data
    session['spring_tmax'] = seasonsForm.spring_tmax.data
    session['summer_tmin'] = seasonsForm.summer_tmin.data
    session['summer_tmax'] = seasonsForm.summer_tmax.data
    session['fall_tmin'] = seasonsForm.fall_tmin.data
    session['fall_tmax'] = seasonsForm.fall_tmax.data
    session['winter_tmin'] = seasonsForm.winter_tmin.data
    session['winter_tmax'] = seasonsForm.winter_tmax.data

def fill_seasons_form():
    seasons_form = seasonsForm(request.form)
    if session.get('year_tmin') is None:
        seasons_form.year_tmin.data = "checked"
        seasons_form.year_tmax.data = "checked"
    else:
        seasons_form.year_tmin.data = session['year_tmin']
        seasons_form.year_tmax.data = session['year_tmax']
        seasons_form.spring_tmin.data = session['spring_tmin']
        seasons_form.spring_tmax.data = session['spring_tmax']
        seasons_form.summer_tmin.data = session['summer_tmin']
        seasons_form.summer_tmax.data = session['summer_tmax']
        seasons_form.fall_tmin.data = session['fall_tmin']
        seasons_form.fall_tmax.data = session['fall_tmax']
        seasons_form.winter_tmin.data = session['winter_tmin']
        seasons_form.winter_tmax.data = session['winter_tmax']
    return seasons_form

def update_and_get_chosen_views(seasonsForm):
    chosen_views = {    
                    'spring':{'TMIN': seasonsForm.spring_tmin.data, 'TMAX': seasonsForm.spring_tmax.data},
                    'summer':{'TMIN': seasonsForm.summer_tmin.data, 'TMAX': seasonsForm.summer_tmax.data},
                    'fall':{'TMIN': seasonsForm.fall_tmin.data, 'TMAX': seasonsForm.fall_tmax.data},
                    'winter':{'TMIN': seasonsForm.winter_tmin.data, 'TMAX': seasonsForm.winter_tmax.data},
                    'year':{'TMIN': seasonsForm.year_tmin.data, 'TMAX': seasonsForm.year_tmax.data}, }
    return chosen_views

@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)
    if request.method == 'GET':
        #Beim ersten mal aufrufen der App
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)
            #Standort Fürth
            form.latitude.data = 49.4771
            form.longitude.data = 10.9887

            current_year = date.today().year
            #Standard-Werte
            form.radius.data = 50
            form.station_count.data = 5
            form.start_year.data = 1960 
            form.end_year.data = current_year
        return render_template('Startseite.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                update_session_form(form)
                session["user_stations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.station_count.data)
            except:
                print("FEHLER")
            return redirect(url_for('list'))   

        else: #Fehlerhaftes Form
            first_key = next(iter(form.errors))
            flash(f"{form.errors[first_key][0]}!")
            
            return render_template("Startseite.html", form=form)

@app.route("/liste", methods=['POST', 'GET'])
def list():
    #Form
    form = searchForm(request.form)
    #Suchfunktion
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                update_session_form(form)
                session["user_stations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.station_count.data)
            except Exception as e:
                flash(f'Unerwarteter Fehler {e}')
                return redirect(url_for('list'))
            return redirect(url_for('list'))
        else:
            first_key = next(iter(form.errors))
            flash(f"{form.errors[first_key][0]}!")
    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)

    
    return render_template('Liste.html',form=form, stations=session["user_stations"])



@app.route("/station/<id>", methods=['POST', 'GET'])
def yearView(id):
    chosen_views = {}
    #Form
    form = searchForm(request.form)
    seasons_form = seasonsForm(request.form)
    

    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button

            
            if seasons_form.validate():
                update_seasons_form(seasons_form)
                chosen_views = update_and_get_chosen_views(seasons_form)
                return redirect(url_for('yearView', id=id))
            else: #Fehlerhaft --> Keine Auswahl getroffen
                return redirect(url_for('yearView', id=id))


        else: #Suchen Button
            if form.validate_on_submit():
                try:
                    update_session_form(form)
                    session["user_stations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.station_count.data)
                    app.stationTemperatures = {}
                except Exception as e:
                    flash(f'Unerwarteter Fehler {e}')
                    return redirect(url_for('list'))
                return redirect(url_for('list'))
            else:
                first_key = next(iter(form.errors))
                flash(f"{form.errors[first_key][0]}!")

    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)
        seasons_form = fill_seasons_form()
        chosen_views = update_and_get_chosen_views(seasons_form)


        #! Folgendes nicht löschen
        
        # #Ermittlung jährlicher Mittelwert
        # if id not in app.stationTemperatures.keys():
        #     stationTemperatures = get_weather_data_of_station_by_station_id(id, session['start_year'], session['end_year'])
        #     stationTemperatures = dict(stationTemperatures)  
        #     app.stationTemperatures = {id:stationTemperatures}

        # if not app.stationTemperatures:
        #     flash('Der ausgewählte Zeitraum enthält keine Daten')
        # else:
        #     #Mittelwerte berechnen
        #     stationTemperatures = app.stationTemperatures[id]                            
        #     averageTemperaturesYear = defaultdict(lambda: defaultdict(lambda: dict()))
        #     #Test Mittelwert Jahr
        #     for year in stationTemperatures:
        #         divisor = 0
        #         sum_min = 0
        #         sum_max = 0
        #         sum_min_spring = 0
        #         sum_max_spring = 0
        #         divisor_spring = 0
        #         sum_min_summer = 0
        #         sum_max_summer = 0
        #         divisor_summer = 0
        #         sum_min_fall = 0
        #         sum_max_fall = 0
        #         divisor_fall = 0

        #         for month in stationTemperatures[year]:
        #             for day in stationTemperatures[year][month]:
        #                 divisor += 1
        #                 sum_min += stationTemperatures[year][month][day]['TMIN']
        #                 sum_max += stationTemperatures[year][month][day]['TMAX']
                        
        #                 if month >= 3 and month <=5: #Frühling
        #                     sum_min_spring += stationTemperatures[year][month][day]['TMIN']
        #                     sum_max_spring += stationTemperatures[year][month][day]['TMAX']
        #                     divisor_spring += 1
                      
        #                 elif month >= 6 and month <= 8: #Sommer
        #                     sum_min_summer += stationTemperatures[year][month][day]['TMIN']
        #                     sum_max_summer += stationTemperatures[year][month][day]['TMAX']
        #                     divisor_summer += 1

        #                 elif month >= 9 and month <= 11: #Herbst
        #                     sum_min_fall += stationTemperatures[year][month][day]['TMIN']
        #                     sum_max_fall += stationTemperatures[year][month][day]['TMAX']
        #                     divisor_fall += 1

        #         averageTemperaturesYear[year]['year']['TMIN'] = round(sum_min/divisor,1)
        #         averageTemperaturesYear[year]['year']['TMAX'] = round(sum_max/divisor,1)

        #         averageTemperaturesYear[year]['spring']['TMIN'] = round(sum_min_spring/divisor_spring,1)
        #         averageTemperaturesYear[year]['spring']['TMAX'] = round(sum_max_spring/divisor_spring,1)

        #         averageTemperaturesYear[year]['summer']['TMIN'] = round(sum_min_summer/divisor_summer,1)
        #         averageTemperaturesYear[year]['summer']['TMAX'] = round(sum_max_summer/divisor_summer,1)

        #         averageTemperaturesYear[year]['fall']['TMIN'] = round(sum_min_fall/divisor_fall,1)
        #         averageTemperaturesYear[year]['fall']['TMAX'] = round(sum_max_fall/divisor_fall,1)

        #         averageTemperaturesYear[year]['winter']['TMIN'] = 2
        #         averageTemperaturesYear[year]['winter']['TMAX'] = 4


    
    #TESTDATEN
    averageTemperaturesYear = {
        1951: {'spring': {'TMIN': 5.2, 'TMAX': 15.3}, 'summer': {'TMIN': 6.3, 'TMAX': 18.5}, 'fall': {'TMIN': 4.8, 'TMAX': 14.2}, 'winter': {'TMIN': 2.1, 'TMAX': 9.8}, 'year': {'TMIN': 4.6, 'TMAX': 14.5}},
        1952: {'spring': {'TMIN': 4.9, 'TMAX': 14.8}, 'summer': {'TMIN': 6.1, 'TMAX': 17.9}, 'fall': {'TMIN': 5.2, 'TMAX': 14.7}, 'winter': {'TMIN': 1.9, 'TMAX': 9.5}, 'year': {'TMIN': 4.8, 'TMAX': 14.2}},
        1953: {'spring': {'TMIN': 5.4, 'TMAX': 15.9}, 'summer': {'TMIN': 6.0, 'TMAX': 18.3}, 'fall': {'TMIN': 5.0, 'TMAX': 15.1}, 'winter': {'TMIN': 2.5, 'TMAX': 10.2}, 'year': {'TMIN': 4.8, 'TMAX': 14.8}},
        1954: {'spring': {'TMIN': 5.1, 'TMAX': 15.4}, 'summer': {'TMIN': 6.2, 'TMAX': 18.7}, 'fall': {'TMIN': 4.9, 'TMAX': 14.4}, 'winter': {'TMIN': 2.0, 'TMAX': 9.7}, 'year': {'TMIN': 4.8, 'TMAX': 14.6}},
        1955: {'spring': {'TMIN': 5.3, 'TMAX': 15.7}, 'summer': {'TMIN': 6.5, 'TMAX': 19.0}, 'fall': {'TMIN': 5.2, 'TMAX': 14.8}, 'winter': {'TMIN': 2.3, 'TMAX': 10.1}, 'year': {'TMIN': 4.8, 'TMAX': 14.9}},
        1956: {'spring': {'TMIN': 5.0, 'TMAX': 15.2}, 'summer': {'TMIN': 6.4, 'TMAX': 18.9}, 'fall': {'TMIN': 5.1, 'TMAX': 14.6}, 'winter': {'TMIN': 2.2, 'TMAX': 9.9}, 'year': {'TMIN': 4.8, 'TMAX': 14.7}},
        1957: {'spring': {'TMIN': 5.5, 'TMAX': 16.1}, 'summer': {'TMIN': 6.7, 'TMAX': 19.4}, 'fall': {'TMIN': 5.4, 'TMAX': 15.3}, 'winter': {'TMIN': 2.7, 'TMAX': 10.4}, 'year': {'TMIN': 4.8, 'TMAX': 15.0}},
        1958: {'spring': {'TMIN': 5.2, 'TMAX': 15.7}, 'summer': {'TMIN': 6.8, 'TMAX': 19.2}, 'fall': {'TMIN': 5.6, 'TMAX': 15.5}, 'winter': {'TMIN': 2.8, 'TMAX': 10.6}, 'year': {'TMIN': 4.8, 'TMAX': 15.1}},
        1959: {'spring': {'TMIN': 5.6, 'TMAX': 16.3}, 'summer': {'TMIN': 7.0, 'TMAX': 19.7}, 'fall': {'TMIN': 5.7, 'TMAX': 15.7}, 'winter': {'TMIN': 3.0, 'TMAX': 10.9}, 'year': {'TMIN': 4.8, 'TMAX': 15.3}},
        1960: {'spring': {'TMIN': 5.4, 'TMAX': 16.0}, 'summer': {'TMIN': 7.2, 'TMAX': 20.0}, 'fall': {'TMIN': 5.5, 'TMAX': 16.0}, 'winter': {'TMIN': 3.2, 'TMAX': 11.2}, 'year': {'TMIN': 4.8, 'TMAX': 15.5}},
        1961: {'spring': {'TMIN': 5.8, 'TMAX': 16.7}, 'summer': {'TMIN': 7.5, 'TMAX': 20.5}, 'fall': {'TMIN': 5.9, 'TMAX': 16.5}, 'winter': {'TMIN': 3.5, 'TMAX': 11.7}, 'year': {'TMIN': 4.8, 'TMAX': 15.8}},
        1962: {'spring': {'TMIN': 5.7, 'TMAX': 16.5}, 'summer': {'TMIN': 7.4, 'TMAX': 20.3}, 'fall': {'TMIN': 5.8, 'TMAX': 16.3}, 'winter': {'TMIN': 3.3, 'TMAX': 11.4}, 'year': {'TMIN': 4.8, 'TMAX': 15.9}},
        1963: {'spring': {'TMIN': 6.1, 'TMAX': 17.2}, 'summer': {'TMIN': 7.8, 'TMAX': 20.9}, 'fall': {'TMIN': 6.0, 'TMAX': 17.0}, 'winter': {'TMIN': 3.8, 'TMAX': 12.0}, 'year': {'TMIN': 4.8, 'TMAX': 16.2}},
    }
    # chosen_views = {'spring':{'TMIN': False, 'TMAX': False},'summer':{'TMIN': False, 'TMAX': False},'fall':{'TMIN': False, 'TMAX': False},'winter':{'TMIN': True, 'TMAX': True},'year':{'TMIN': True, 'TMAX': True}, }
    script, div = DiagramPloter.plotYearDiagram(averageTemperaturesYear, chosen_views)

    return render_template('Jahresansicht.html',form=form,seasons_form=seasons_form,averageTemperaturesYear = averageTemperaturesYear, id=id, script=script, div=div)

@app.route("/station/<id>/<year>")
def monthView(id, year):
    year = int(year)
    #Suchfunktion
    if request.method == 'POST' and form.validate_on_submit():
        try:
            session["user_stations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.station_count.data)
            update_session_form(form)
        except:
            print(f"FEHLER:")
            return redirect()
        return redirect(url_for('list'))
    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)

    averageTemperaturesMonthly = defaultdict(lambda: dict())
    # #Testdata monthly
    averageTemperaturesMonthly = {
        1: {'TMIN': 4.3, 'TMAX': 14.7},
        2: {'TMIN': 5.1, 'TMAX': 15.2},
        3: {'TMIN': 3.8, 'TMAX': 14.5},
        4: {'TMIN': 6.2, 'TMAX': 16.8},
        5: {'TMIN': 4.5, 'TMAX': 15.0},
        6: {'TMIN': 5.3, 'TMAX': 15.7},
        7: {'TMIN': 4.8, 'TMAX': 14.9},
        8: {'TMIN': 6.0, 'TMAX': 16.5},
        9: {'TMIN': 5.7, 'TMAX': 15.4},
        10: {'TMIN': 4.1, 'TMAX': 14.2},
        11: {'TMIN': 5.6, 'TMAX': 15.8},
        12: {'TMIN': 4.9, 'TMAX': 15.1}
    }

    #Ermittlung monatlicher Mittelwert
    # stationTemperatures = session['station_weather_data_selected_period'] 
    # stationTemperatures = dict(stationTemperatures)

    # monthlyRaw = stationTemperatures[year]

    # for month in monthlyRaw:
    #     divisor = 0
    #     sumMin = 0
    #     sumMax = 0
    #     for day in monthlyRaw[month]:
    #             divisor += 1
    #             sumMin += monthlyRaw[month][day]['TMIN']
    #             sumMax += monthlyRaw[month][day]['TMAX']
    #     averageTemperaturesMonthly[month]['TMIN'] = round(sumMin/divisor,1)
    #     averageTemperaturesMonthly[month]['TMAX'] = round(sumMax/divisor,1)

    

    script, div = DiagramPloter.plotMonthDiagram(averageTemperaturesMonthly, True, True)

    return render_template('Monatsansicht.html', averageTemperaturesMonthly = averageTemperaturesMonthly, id=id, form=form, script=script, div=div, year=year)

@app.route("/station/<id>/<year>/<month>")
def dayView(id,year,month):
    
    #Suchfunktion
    if request.method == 'POST' and form.validate_on_submit():
        try:
            session["user_stations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.station_count.data)
            update_session_form(form)
        except:
            print(f"FEHLER:")
            return redirect()
        return redirect(url_for('list'))
    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)

    #Tageswerte ermitteln
    # stationTemperatures = session['station_weather_data_selected_period'] 
    # stationTemperatures = dict(stationTemperatures)
    # temperatures_daily = stationTemperatures[year][month]
 
    #Testdaten
    temperatures_daily = { 
    1: {'TMIN': 4.3, 'TMAX': 14.7},
    2: {'TMIN': 4.1, 'TMAX': 15.0},
    3: {'TMIN': 3.8, 'TMAX': 14.5},
    4: {'TMIN': 4.5, 'TMAX': 14.8},
    5: {'TMIN': 4.0, 'TMAX': 15.2},
    6: {'TMIN': 3.7, 'TMAX': 14.9},
    7: {'TMIN': 4.2, 'TMAX': 14.6},
    8: {'TMIN': 3.9, 'TMAX': 15.1},
    9: {'TMIN': 4.4, 'TMAX': 14.4},
    10: {'TMIN': 3.6, 'TMAX': 15.3},
    11: {'TMIN': 4.3, 'TMAX': 14.7},
    12: {'TMIN': 4.1, 'TMAX': 15.0},
    13: {'TMIN': 3.8, 'TMAX': 14.5},
    14: {'TMIN': 4.5, 'TMAX': 14.8},
    15: {'TMIN': 4.0, 'TMAX': 15.2},
    16: {'TMIN': 3.7, 'TMAX': 14.9},
    17: {'TMIN': 4.2, 'TMAX': 14.6},
    18: {'TMIN': 3.9, 'TMAX': 15.1},
    19: {'TMIN': 4.4, 'TMAX': 14.4},
    20: {'TMIN': 3.6, 'TMAX': 15.3},
    21: {'TMIN': 4.3, 'TMAX': 14.7},
    22: {'TMIN': 4.1, 'TMAX': 15.0},
    23: {'TMIN': 3.8, 'TMAX': 14.5},
    24: {'TMIN': 4.5, 'TMAX': 14.8},
    25: {'TMIN': 4.0, 'TMAX': 15.2},
    26: {'TMIN': 3.7, 'TMAX': 14.9},
    27: {'TMIN': 4.2, 'TMAX': 14.6},
    28: {'TMIN': 3.9, 'TMAX': 15.1},
    29: {'TMIN': 4.4, 'TMAX': 14.4},
    30: {'TMIN': 3.6, 'TMAX': 15.3},
    31: {'TMIN': 4.3, 'TMAX': 14.7}
}
    script, div = DiagramPloter.plotDayDiagram(temperatures_daily, True, True)

    return render_template('Tagesansicht.html', form=form, temperatures_daily=temperatures_daily, script=script, div=div)


if __name__ == '__main__':
    app.run(debug=False) #changed because of performance