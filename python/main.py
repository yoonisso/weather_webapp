from flask import Flask, render_template, request, flash, redirect, url_for, session, Response
from forms import searchForm, seasonsFormClass
import secrets
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
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

#START BEISPIEL
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
#ENDE BESIPIEL

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
    
    # if(session.get('latitude') is not None):
    #     form = fill_form()
    # else:
    #     form = searchForm(request.form)

    #Suchfunktion
    if request.method == 'POST' and form.validate_on_submit():
        try:
            session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
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

    return render_template('Liste.html',form=form, stations=session["user_stations"])

@app.route("/station/<id>", methods=['GET', 'POST'])
def yearView(id):
    seasonsForm = seasonsFormClass(request.form)
    seasonsForm.year_tmin.data = "checked"
    seasonsForm.year_tmax.data = "checked"
    

    # if request.form.get('action') == 'search_icon':
    #     print('HALLOO')

    if request.method == 'POST': 
        if request.form['action'] == 'Search':
            if  form.validate_on_submit():
                try:
                    session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
                    update_session_form(form)
                except:
                    print(f"FEHLER:")
                    return redirect()
                return redirect(url_for('list'))

        elif request.form['action'] == 'Aktualisieren':
            if seasonsForm.validate():
                 chosen_views = {'spring':{'TMIN': seasonsForm.spring_tmin.data, 'TMAX': seasonsForm.spring_tmax.data},'summer':{'TMIN': True, 'TMAX': True},'fall':{'TMIN': True, 'TMAX': True},'winter':{'TMIN': True, 'TMAX': True},'spring':{'TMIN': True, 'TMAX': True}, }
       
    
    elif request.method == 'GET':
        if(session.get('latitude') is not None):
            form = fill_form()
        else:
            form = searchForm(request.form)

        #! Folgendes nicht löschen
        
        #Ermittlung jährlicher Mittelwert
        # stationTemperatures = get_weather_data_of_station_by_station_id(id, session['startYear'], session['endYear'])
        # stationTemperatures = dict(stationTemperatures)

        # if not stationTemperatures:
        #     flash('Der ausgewählte Zeitraum enthält keine Daten')
        # else:
        #     session['station_weather_data_selected_period'] = stationTemperatures #TODO: Dieser ansatz oder bei jeder Seite Daten neu laden, damit auch eine Navigation über Adresszeile öglich wäre??
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


    # chosen_views = {'spring':{'TMIN': True, 'TMAX': True},'summer':{'TMIN': True, 'TMAX': True},'fall':{'TMIN': True, 'TMAX': True},'winter':{'TMIN': True, 'TMAX': True},'spring':{'TMIN': True, 'TMAX': True}, }
    script, div = DiagramPloter.plotDiagram(averageTemperaturesYear, "Jahresansicht", "Jahre")

    return render_template('Jahresansicht.html',form=form,seasonsForm=seasonsForm,averageTemperaturesYear = averageTemperaturesYear, id=id, script=script, div=div)

@app.route("/<id>/<year>")
def monthView(id, year):
    year = int(year)
    #Suchfunktion
    if request.method == 'POST' and form.validate_on_submit():
        try:
            session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
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

    

    script, div = DiagramPloter.plotDiagram(averageTemperaturesMonthly, "Monatsansicht", "Monate") #TODO change x_axis of month to jan. feb. view

    return render_template('Monatsansicht.html', averageTemperaturesMonthly = averageTemperaturesMonthly, id=id, form=form, script=script, div=div, year=year)

@app.route("/<id>/<year>/<month>")
def dayView(id,year,month):
    
    #Suchfunktion
    if request.method == 'POST' and form.validate_on_submit():
        try:
            session["userStations"] = SearchData.getStations(form.latitude.data, form.longitude.data, form.radius.data, form.stationCount.data)
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

    return render_template('Tagesansicht.html', form=form, temperatures_daily=temperatures_daily)


if __name__ == '__main__':
    app.run(debug=False) #changed because of performance