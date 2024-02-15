from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import searchForm, seasonsForm, minMaxForm, update_form_session, fill_form, update_seasons_sessions, fill_seasons_form, update_min_max_session, fill_min_max_form, update_and_get_chosen_views
import secrets
from datetime import date
from helpers.diagram_ploter import DiagramPloter
from collections import defaultdict
from api_caller import get_stations_by_coordinates, load_all_stations

#TODO: FORM link auf jeweilige Seite anpassen + POST handling

secret_key = secrets.token_urlsafe(16)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secret_key

#Initialization
app.all_stations = load_all_stations()
app.station_temperatures = {}

@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)
    if request.method == 'GET':
        form = fill_form()
        return render_template('Startseite.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                update_form_session(form)
                session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
            except Exception as e:
                flash(f'Unerwarteter Fehler: {e}')
                return redirect(url_for('list'))
            return redirect(url_for('list'))

        else: #Fehlerhaftes Form
            first_key = next(iter(form.errors))
            flash(f"{form.errors[first_key][0]}!")
            
            return render_template("Startseite.html", form=form)

@app.route("/liste", methods=['POST', 'GET'])
def list():
    form = searchForm(request.form) #Nur notwendig, wenn man über Adresszeile navigiert??
    #Suchfunktion
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                update_form_session(form)
                session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
            except Exception as e:
                flash(f'Unerwarteter Fehler {e}')
                return redirect(url_for('list'))
            return redirect(url_for('list'))
        else:
            first_key = next(iter(form.errors))
            flash(f"{form.errors[first_key][0]}!")
    
    elif request.method == 'GET':
        form = fill_form()

    return render_template('Liste.html',form=form, stations=session["user_stations"])

@app.route("/station/<id>", methods=['POST', 'GET'])
def yearlyView(id):
    #Form
    form = searchForm(request.form)
    seasons_form = seasonsForm(request.form)

    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            
            if seasons_form.validate():
                update_seasons_sessions(seasons_form)
                session['chosen_views'] = update_and_get_chosen_views(seasons_form)
                return redirect(url_for('yearlyView', id=id))
            else: #Fehlerhaft --> Keine Auswahl getroffen
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
                return redirect(url_for('yearlyView', id=id))


        else: #Suchen Button
            if form.validate_on_submit():
                try:
                    update_form_session(form)
                    session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                    app.station_temperatures = {}
                except Exception as e:
                    flash(f'Unerwarteter Fehler {e}')
                    return redirect(url_for('list'))
                return redirect(url_for('list'))
            else:
                first_key = next(iter(form.errors))
                flash(f"{form.errors[first_key][0]}!")

    
    # elif request.method == 'GET':
   
        
        #! Folgendes nicht löschen
        
        # #Ermittlung jährlicher Mittelwert
        # if id not in app.station_temperatures.keys():
        #     station_temperatures = get_weather_data_of_station_by_station_id(id, session['start_year'], session['end_year'])
        #     station_temperatures = dict(station_temperatures)  
        #     app.station_temperatures = {id:station_temperatures}

        # if not app.station_temperatures:
        #     flash('Der ausgewählte Zeitraum enthält keine Daten')
        # else:
        #     #Mittelwerte berechnen
        #     station_temperatures = app.station_temperatures[id]                            
        #     averageTemperaturesYear = defaultdict(lambda: defaultdict(lambda: dict()))
        #     #Test Mittelwert Jahr
        #     for year in station_temperatures:
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

        #         for month in station_temperatures[year]:
        #             for day in station_temperatures[year][month]:
        #                 divisor += 1
        #                 sum_min += station_temperatures[year][month][day]['TMIN']
        #                 sum_max += station_temperatures[year][month][day]['TMAX']
                        
        #                 if month >= 3 and month <=5: #Frühling
        #                     sum_min_spring += station_temperatures[year][month][day]['TMIN']
        #                     sum_max_spring += station_temperatures[year][month][day]['TMAX']
        #                     divisor_spring += 1
                      
        #                 elif month >= 6 and month <= 8: #Sommer
        #                     sum_min_summer += station_temperatures[year][month][day]['TMIN']
        #                     sum_max_summer += station_temperatures[year][month][day]['TMAX']
        #                     divisor_summer += 1

        #                 elif month >= 9 and month <= 11: #Herbst
        #                     sum_min_fall += station_temperatures[year][month][day]['TMIN']
        #                     sum_max_fall += station_temperatures[year][month][day]['TMAX']
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


    form = fill_form()
    seasons_form = fill_seasons_form()

    if(session.get('chosen_views') is None):
        chosen_views = update_and_get_chosen_views(seasons_form)
    else:
        chosen_views = session['chosen_views']
    
    script, div = DiagramPloter.plotYearDiagram(averageTemperaturesYear, chosen_views, f"http://127.0.0.1:5000/station/{id}")

    return render_template('Jahresansicht.html',form=form,seasons_form=seasons_form,averageTemperaturesYear = averageTemperaturesYear, id=id, script=script, div=div)

@app.route("/station/<id>/<year>", methods=['POST', 'GET'])
def monthlyView(id, year):
    year = int(year)
    min_max_form = minMaxForm(request.form)
    
    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            if min_max_form.validate(): #Mindestens eine Auswahl getroffen
                update_min_max_session(min_max_form)
            else:
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
            return redirect(url_for('monthlyView', id=id, year=year))
        #Suchfunktion
        elif form.validate_on_submit():
            try:
                session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                update_form_session(form)
            except:
                print(f"FEHLER:")
                return redirect()
        return redirect(url_for('list'))
    
    elif request.method == 'GET':
        form = fill_form()
        min_max_form = fill_min_max_form()

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
    # station_temperatures = session['station_weather_data_selected_period'] 
    # station_temperatures = dict(station_temperatures)

    # monthlyRaw = station_temperatures[year]

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

    

    script, div = DiagramPloter.plotMonthDiagram(averageTemperaturesMonthly, min_max_form.year_tmin.data, min_max_form.year_tmax.data,f"http://127.0.0.1:5000/station/{id}/{year}")

    return render_template('Monatsansicht.html', averageTemperaturesMonthly = averageTemperaturesMonthly, id=id, form=form,min_max_form=min_max_form, script=script, div=div, year=year)

@app.route("/station/<id>/<year>/<month>", methods=['POST', 'GET'])
def daylyView(id,year,month):
    
    min_max_form = minMaxForm(request.form)
    #Suchfunktion
    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            if min_max_form.validate(): #Mindestens eine Auswahl getroffen
                update_min_max_session(min_max_form)
            else:
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
            return redirect(url_for('monthlyView', id=id, year=year, month=month))
        elif form.validate_on_submit(): #Suchfunktion
            try:
                session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                update_form_session(form)
            except:
                print(f"FEHLER:")
                return redirect()
            return redirect(url_for('list'))
    
    elif request.method == 'GET':
        form = fill_form()
        min_max_form = fill_min_max_form()

    #Tageswerte ermitteln
    # station_temperatures = session['station_weather_data_selected_period'] 
    # station_temperatures = dict(station_temperatures)
    # temperatures_daily = station_temperatures[year][month]
 
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
    script, div = DiagramPloter.plotDayDiagram(temperatures_daily, min_max_form.year_tmin.data, min_max_form.year_tmax.data)

    return render_template('Tagesansicht.html', form=form,min_max_form=min_max_form, temperatures_daily=temperatures_daily, script=script, div=div,id=id, year=year, month=month)

if __name__ == '__main__':
    app.run(debug=False) #changed because of performance