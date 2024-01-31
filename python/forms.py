from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField, FloatField, DecimalRangeField
from wtforms.validators import DataRequired, NumberRange

class searchForm(FlaskForm):
    longitude = FloatField('Längengrad') 
    latitude = FloatField('Breitengrad')
    valueRange =  DecimalRangeField('Radius', validators = [NumberRange(5, 100)])
    startYear = IntegerField('Startjahr', validators = [NumberRange(1800, 2999)])
    endYear = IntegerField('Endjahr', validators = [NumberRange(1800, 2999)])
    stationCount = IntegerField('Anzahl Stationen', validators= [NumberRange(1, 20)])