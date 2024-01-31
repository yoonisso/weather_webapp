from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField, FloatField, DecimalRangeField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class MyFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid float value'))

class searchForm(FlaskForm):
    longitude = DecimalField('Längengrad', places=6) 
    latitude = DecimalField('Breitengrad', places=6)
    radius =  DecimalRangeField('Radius', validators = [NumberRange(5, 100)])
    startYear = IntegerField('Startjahr', validators = [NumberRange(1800, 2999)])
    endYear = IntegerField('Endjahr', validators = [NumberRange(1800, 2999)])
    stationCount = IntegerField('Anzahl Stationen', validators= [NumberRange(1, 20)])

