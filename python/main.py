from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import searchForm, seasonsForm, minMaxForm, update_form_session, fill_form, update_seasons_sessions, fill_seasons_form, update_min_max_session, fill_min_max_form, update_and_get_chosen_views
import secrets
from helpers.diagram_ploter import DiagramPloter
from collections import defaultdict
from api_caller import get_stations_by_coordinates, load_all_stations, get_weather_data_of_station_by_station_id

#Initialization
secret_key = secrets.token_urlsafe(16)
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secret_key

app.all_stations = load_all_stations()
app.all_stations_temperatures = {}
app.station_selected_period = {}

def search_stations(form, redirect_on_error):
    """
    Search stations and navigates to list route to show stations
    Args:
        form: Search criteria
        redirect_on_error: route to be navigated to in case of error
    Returns:
        redirect to given route
    """
    update_form_session(form)
    if form.validate():
        try:
            session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
        except Exception as e:
            flash(f'Unerwarteter Fehler: {e}')
            return redirect(url_for(redirect_on_error))
        return redirect(url_for('list'))
    else: #Fehlerhaftes Form
        first_key = next(iter(form.errors))
        flash(f"{form.errors[first_key][0]}!")
        return redirect(url_for(redirect_on_error))

@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)
    if request.method == 'POST':
        return search_stations(form,'home')
    elif request.method == 'GET':
        form = fill_form()
    return render_template('Startseite.html', form=form)

@app.route("/liste", methods=['POST', 'GET'])
def list():
    form = searchForm(request.form)
    #Suchfunktion
    if request.method == 'POST':
        search_stations(form, 'list')
    elif request.method == 'GET':
        form = fill_form()
    return render_template('Liste.html',form=form, stations=session["user_stations"])

@app.route("/station/<id>", methods=['POST', 'GET'])
def yearly_view(id):
    #Form
    form = searchForm(request.form)
    seasons_form = seasonsForm(request.form)

    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            
            if seasons_form.validate():
                update_seasons_sessions(seasons_form)
                session['chosen_views'] = update_and_get_chosen_views(seasons_form)
                return redirect(url_for('yearly_view', id=id))
            else: #Fehlerhaft --> Keine Auswahl getroffen
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
                return redirect(url_for('yearly_view', id=id))

        else: #Suchen Button
            update_form_session(form)
            if form.validate():
                try:
                    session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                except Exception as e:
                    flash(f'Unerwarteter Fehler: {e}')
                    return redirect(url_for('yearly_view', id=id))
                return redirect(url_for('list'))
            else: #Fehlerhaftes Form
                first_key = next(iter(form.errors))
                flash(f"{form.errors[first_key][0]}!")
                return redirect(url_for('yearly_view', id=id))
    
    elif request.method == 'GET':        
        #Ermittlung Wetterdaten
        if id not in app.all_stations_temperatures.keys():
            app.all_stations_temperatures[id] = dict(get_weather_data_of_station_by_station_id(id))

        #Jahresfilter
        station_selected_period = {}
        start_year = session['start_year']
        end_year = session['end_year']
        all_station_temperatures = app.all_stations_temperatures[id]
        for year in all_station_temperatures:
            if year >= start_year and year <= end_year:
                station_selected_period[year] = all_station_temperatures[year]

        if len(station_selected_period.keys()) == 0:
            flash('Die Station enthält für den ausgewählten Zeitraum keine Daten')
            return redirect(url_for('list'))
            
        else:
            #Mittelwerte berechnen        
            average_temperatures_year = defaultdict(lambda: defaultdict(lambda: dict()))
            for year in station_selected_period:
                divisor = 0
                sum_min = 0
                sum_max = 0
                sum_min_spring = 0
                sum_max_spring = 0
                divisor_spring = 0
                sum_min_summer = 0
                sum_max_summer = 0
                divisor_summer = 0
                sum_min_fall = 0
                sum_max_fall = 0
                divisor_fall = 0
                sum_min_winter = 0
                sum_max_winter = 0
                divisor_winter = 0

                for month in station_selected_period[year]:
                    for day in station_selected_period[year][month]:
                        if 'TMIN' in station_selected_period[year][month][day].keys() and 'TMAX' in station_selected_period[year][month][day].keys():
                            divisor += 1
                            sum_min += station_selected_period[year][month][day]['TMIN']
                            sum_max += station_selected_period[year][month][day]['TMAX']

                            
                            if month >= 3 and month <=5: #Frühling
                                sum_min_spring += station_selected_period[year][month][day]['TMIN']
                                sum_max_spring += station_selected_period[year][month][day]['TMAX']
                                divisor_spring += 1
                        
                            elif month >= 6 and month <= 8: #Sommer
                                sum_min_summer += station_selected_period[year][month][day]['TMIN']
                                sum_max_summer += station_selected_period[year][month][day]['TMAX']
                                divisor_summer += 1

                            elif month >= 9 and month <= 11: #Herbst
                                sum_min_fall += station_selected_period[year][month][day]['TMIN']
                                sum_max_fall += station_selected_period[year][month][day]['TMAX']
                                divisor_fall += 1
                            elif month == 1 or month == 2: #Winter
                                sum_min_winter += station_selected_period[year][month][day]['TMIN']
                                sum_max_winter += station_selected_period[year][month][day]['TMAX']
                                divisor_winter += 1
                            elif month == 12: #Winter vom Vorjahr
                                if year-1 in all_station_temperatures.keys():
                                    if 'TMIN' in all_station_temperatures[year-1][month][day].keys() and 'TMAX' in all_station_temperatures[year-1][month][day].keys():
                                        sum_min_winter += all_station_temperatures[year-1][month][day]['TMIN']
                                        sum_max_winter += all_station_temperatures[year-1][month][day]['TMAX']
                                        divisor_winter += 1

                if divisor == 0:
                    divisor = 1
                average_temperatures_year[year]['year']['TMIN'] = round(sum_min/divisor,1)
                average_temperatures_year[year]['year']['TMAX'] = round(sum_max/divisor,1)

                if divisor_spring == 0:
                    divisor_spring = 1
                average_temperatures_year[year]['spring']['TMIN'] = round(sum_min_spring/divisor_spring,1)
                average_temperatures_year[year]['spring']['TMAX'] = round(sum_max_spring/divisor_spring,1)

                if divisor_summer == 0:
                    divisor_summer = 1
                average_temperatures_year[year]['summer']['TMIN'] = round(sum_min_summer/divisor_summer,1)
                average_temperatures_year[year]['summer']['TMAX'] = round(sum_max_summer/divisor_summer,1)

                if divisor_fall == 0:
                    divisor_fall = 1
                average_temperatures_year[year]['fall']['TMIN'] = round(sum_min_fall/divisor_fall,1)
                average_temperatures_year[year]['fall']['TMAX'] = round(sum_max_fall/divisor_fall,1)

                if divisor_winter == 0:
                    divisor_winter = 1
                average_temperatures_year[year]['winter']['TMIN'] = round(sum_min_winter/divisor_winter,1)
                average_temperatures_year[year]['winter']['TMAX'] = round(sum_max_winter/divisor_winter,1)
    
    form = fill_form()
    seasons_form = fill_seasons_form()

    if(session.get('chosen_views') is None):
        chosen_views = update_and_get_chosen_views(seasons_form)
    else:
        chosen_views = session['chosen_views']
    
    script, div = DiagramPloter.plotYearDiagram(average_temperatures_year, chosen_views, f"http://127.0.0.1:5000/station/{id}")

    return render_template('Jahresansicht.html',form=form,seasons_form=seasons_form,average_temperatures_year = average_temperatures_year, id=id, script=script, div=div)

@app.route("/station/<id>/<year>", methods=['POST', 'GET'])
def monthly_view(id, year):
    year = int(year)
    #Form
    min_max_form = minMaxForm(request.form)
    form = searchForm(request.form)
    
    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            if min_max_form.validate(): #Mindestens eine Auswahl getroffen
                update_min_max_session(min_max_form)
            else:
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
            return redirect(url_for('monthly_view', id=id, year=year))
        else: #Suchfunktion
            update_form_session(form)
            if form.validate():
                try:
                    session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                except Exception as e:
                    flash(f'Unerwarteter Fehler: {e}')
                    return redirect(url_for('monthly_view', id=id, year=year))
                return redirect(url_for('list'))
            else: #Fehlerhaftes Form
                first_key = next(iter(form.errors))
                flash(f"{form.errors[first_key][0]}!")
                return redirect(url_for('monthly_view', id=id, year=year))
            
    elif request.method == 'GET':
        form = fill_form()
        min_max_form = fill_min_max_form()
    
    averageTemperaturesMonthly = defaultdict(lambda: dict())

    #Ermittlung monatlicher Mittelwert
    all_stations_temperatures = app.all_stations_temperatures
    all_stations_temperatures = dict(all_stations_temperatures)

    monthly_raw = all_stations_temperatures[id][year]

    for month in monthly_raw:
        divisor = 0
        sumMin = 0
        sumMax = 0
        for day in monthly_raw[month]:
                divisor += 1
                if 'TMIN' in  monthly_raw[month][day].keys():
                    sumMin += monthly_raw[month][day]['TMIN']
                if 'TMAX' in  monthly_raw[month][day].keys():
                    sumMax += monthly_raw[month][day]['TMAX']
        averageTemperaturesMonthly[month]['TMIN'] = round(sumMin/divisor,1)
        averageTemperaturesMonthly[month]['TMAX'] = round(sumMax/divisor,1)

    script, div = DiagramPloter.plotMonthDiagram(averageTemperaturesMonthly, min_max_form.year_tmin.data, min_max_form.year_tmax.data,f"http://127.0.0.1:5000/station/{id}/{year}")

    return render_template('Monatsansicht.html', averageTemperaturesMonthly = averageTemperaturesMonthly, id=id, form=form,min_max_form=min_max_form, script=script, div=div, year=year)

@app.route("/station/<id>/<year>/<month>", methods=['POST', 'GET'])
def daily_view(id,year,month):
    year = int(year)
    month = int(month)
    #Form
    form = searchForm(request.form)
    min_max_form = minMaxForm(request.form)
    #Suchfunktion
    if request.method == 'POST':
        if request.form.get('action'): #Aktualisieren Button
            if min_max_form.validate(): #Mindestens eine Auswahl getroffen
                update_min_max_session(min_max_form)
            else:
                flash("Es muss mindestens eine Sicht ausgewählt werden!")
            return redirect(url_for('daily_view', id=id, year=year, month=month))
        else: #Suchfunktion
            update_form_session(form)
            if form.validate():
                try:
                    session["user_stations"] = get_stations_by_coordinates(app.all_stations,form.latitude.data,form.longitude.data,form.radius.data,form.station_count.data)
                except Exception as e:
                    flash(f'Unerwarteter Fehler: {e}')
                    return redirect(url_for('daily_view',id=id,year=year,month=month))
                return redirect(url_for('list'))
            else: #Fehlerhaftes Form
                first_key = next(iter(form.errors))
                flash(f"{form.errors[first_key][0]}!")
                return redirect(url_for('daily_view',id=id,year=year,month=month))
    
    elif request.method == 'GET':
        form = fill_form()
        min_max_form = fill_min_max_form()

    #Tageswerte ermitteln
    # all_stations_temperatures = session['station_weather_data_selected_period'] 
    all_stations_temperatures = app.all_stations_temperatures
    all_stations_temperatures = dict(all_stations_temperatures)

    monthly_raw = dict(all_stations_temperatures[id][year])
    temperatures_daily = monthly_raw[month]
    temperatures_daily = dict(sorted(temperatures_daily.items()))

    script, div = DiagramPloter.plotDayDiagram(temperatures_daily, min_max_form.year_tmin.data, min_max_form.year_tmax.data)

    return render_template('Tagesansicht.html', form=form,min_max_form=min_max_form, temperatures_daily=temperatures_daily, script=script, div=div,id=id, year=year, month=month)

if __name__ == '__main__':
    app.run(debug=False) #changed because of performance