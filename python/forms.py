from flask_wtf import FlaskForm
from wtforms import IntegerField,DecimalField, IntegerRangeField, BooleanField, SubmitField
from wtforms.validators import NumberRange,InputRequired, ValidationError
from datetime import date
from flask import session, request

class searchForm(FlaskForm):

    def validate_year(form, field):
        if(form.start_year.data > form.end_year.data):
            raise ValidationError('Endjahr muss größer oder gleich Startjahr sein')
        current_year = date.today().year
        if(form.start_year.data > current_year):
            raise ValidationError('Startjahr liegt in der Zukunft')
        if(form.end_year.data > current_year):
            raise ValidationError('Endjahr liegt in der Zukunft')

    latitude = DecimalField('Breitengrad', places=6, validators=[InputRequired(message="Bitte Breitengrad angeben"), NumberRange(-90,90, message="Bitte gültigen Breitengrad angeben. Breitengrad muss zwischen -90 und 90 liegen.")])
    longitude = DecimalField('Längengrad', places=6, validators=[InputRequired(message="Bitte Längengrad angeben"), NumberRange(-180,180,message="Bitte gültigen Längengrad angeben. Längengrad muss zwischen -180 und 180 liegen.")]) 
    radius =  IntegerRangeField('Radius', validators = [NumberRange(1, 100),InputRequired(message="Bitte Radius angeben")] )
    start_year = IntegerField('Startjahr', validators = [NumberRange(1800, 2999), InputRequired(message="Bitte Startjahr angeben")])
    end_year = IntegerField('Endjahr', validators = [NumberRange(1800, 2999), InputRequired(message="Bitte Endjahr angeben"), validate_year])
    station_count = IntegerField('Anzahl Stationen', validators= [NumberRange(1, 20, message="Anzahl Stationen muss zwischen 1 und 20 sein"), InputRequired("Bitte Anzahl Stationen angeben")])

class seasonsForm(FlaskForm):
    def minimum_one_selected(form,field):
        if(      form.year_tmin.data == False
            and  form.year_tmax.data == False
            and  form.spring_tmin.data == False
            and  form.spring_tmax.data == False
            and  form.summer_tmin.data == False
            and  form.summer_tmax.data == False
            and  form.fall_tmin.data == False
            and  form.fall_tmax.data == False
            and  form.winter_tmin.data == False
            and  form.winter_tmax.data == False
        ):
            raise ValidationError("Bitte mindestens eine Auswahl treffen!")

    year_tmin       = BooleanField(default="checked",validators=[minimum_one_selected])
    year_tmax      = BooleanField(default="true")
    spring_tmin     = BooleanField()
    spring_tmax     = BooleanField()
    summer_tmin     = BooleanField()
    summer_tmax    = BooleanField()
    fall_tmin       = BooleanField()
    fall_tmax      = BooleanField()
    winter_tmin     = BooleanField()
    winter_tmax    = BooleanField()
    submit_field = SubmitField('Aktualisieren',name="action")

class minMaxForm(FlaskForm):
    def minimum_one_selected(form,field):
        if form.year_tmin.data == False and form.year_tmax.data == False:
            raise ValidationError("Bitte mindestens eine Auswahl treffen!")
        
    year_tmin = BooleanField(default="checked",validators=[minimum_one_selected])
    year_tmax = BooleanField(default="checked")
    submit_field = SubmitField('Aktualisieren',name="action")


def fill_form():
    form = searchForm(request.form)
    if(session.get('latitude') is not None):
        form.latitude.data = float(session['latitude'])
        form.longitude.data = float(session['longitude'])
        form.radius.data = session['radius']
        form.station_count.data = session['station_count']
        form.start_year.data = session['start_year']
        form.end_year.data = session['end_year']
    else:
            #Standort Fürth
            form.latitude.data = 49.4771
            form.longitude.data = 10.9887
            current_year = date.today().year
            #Standard-Werte
            form.radius.data = 50
            form.station_count.data = 5
            form.start_year.data = 1960 
            form.end_year.data = current_year
    return form


def update_form_session(form):
    #Update Session (Form)
    session['latitude'] = form.latitude.data
    session['longitude'] = form.longitude.data
    session['radius'] = form.radius.data
    session['station_count'] = form.station_count.data
    session['start_year'] = form.start_year.data
    session['end_year'] = form.end_year.data

def update_seasons_sessions(seasonsForm):
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

def update_min_max_session(min_max_form):
    session['show_tmin'] = min_max_form.year_tmin.data
    session['show_tmax'] = min_max_form.year_tmax.data

def fill_min_max_form():
    min_max_form = minMaxForm(request.form)
    if session.get('show_tmin') is None:
        min_max_form.year_tmin.data = "checked"
        min_max_form.year_tmax.data = "checked"
    else:
        min_max_form.year_tmin.data = session['show_tmin']
        min_max_form.year_tmax.data = session['show_tmax']
    return min_max_form

def update_and_get_chosen_views(seasonsForm):
    chosen_views = {    
                    'spring':{'TMIN': seasonsForm.spring_tmin.data, 'TMAX': seasonsForm.spring_tmax.data},
                    'summer':{'TMIN': seasonsForm.summer_tmin.data, 'TMAX': seasonsForm.summer_tmax.data},
                    'fall':{'TMIN': seasonsForm.fall_tmin.data, 'TMAX': seasonsForm.fall_tmax.data},
                    'winter':{'TMIN': seasonsForm.winter_tmin.data, 'TMAX': seasonsForm.winter_tmax.data},
                    'year':{'TMIN': seasonsForm.year_tmin.data, 'TMAX': seasonsForm.year_tmax.data}, }
    return chosen_views