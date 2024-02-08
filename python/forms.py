from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField, FloatField, DecimalRangeField, DecimalField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange,InputRequired, ValidationError
from datetime import date

# class MyFloatField(FloatField):
#     def process_formdata(self, valuelist): #TODO: Wird überhaupt verwendet?
#         if valuelist:
#             try:
#                 self.data = float(valuelist[0].replace(',', '.'))
#             except ValueError:
#                 self.data = None
#                 raise ValueError(self.gettext('Not a valid float value'))

class searchForm(FlaskForm):

    def validate_year(form, field):
        if(form.start_year.data > form.end_year.data):
            raise ValidationError('Endjahr muss größer oder gleich Startjahr sein')
        current_year = date.today().year
        if(form.start_year.data > current_year):
            raise ValidationError('Startjahr liegt in der Zukunft')
        if(form.end_year.data > current_year):
            raise ValidationError('Endjahr liegt in der Zukunft')

    latitude = DecimalField('Breitengrad', places=6, validators=[InputRequired(message="Bitte Breitengrad angeben!")])
    longitude = DecimalField('Längengrad', places=6, validators=[InputRequired(message="Bitte Längengrad angeben!")]) 
    radius =  IntegerRangeField('Radius', validators = [NumberRange(1, 100),InputRequired(message="Bitte Radius angeben!")] )
    start_year = IntegerField('Startjahr', validators = [NumberRange(1800, 2999), InputRequired(message="Bitte Startjahr angeben!")])
    end_year = IntegerField('Endjahr', validators = [NumberRange(1800, 2999), InputRequired(message="Bitte Endjahr angeben!"), validate_year])
    station_count = IntegerField('Anzahl Stationen', validators= [NumberRange(1, 20), InputRequired("Bitte Anzahl Stationen angeben!")])

  

