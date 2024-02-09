from flask_wtf import FlaskForm
from wtforms import IntegerField,DecimalField, IntegerRangeField, BooleanField, SubmitField
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

class seasonsFormClass(FlaskForm):

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


