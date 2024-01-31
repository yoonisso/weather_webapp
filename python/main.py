from flask import Flask, render_template, request, flash, redirect, url_for
from forms import searchForm
import secrets

secret_key = secrets.token_urlsafe(16)



app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secret_key

class searchData:
    def __init__(self,longitude,latitude,radius,startYear,endYear,stationCount):
        self.longitude = longitude
        self.latitude = latitude
        self.radius = radius
        self.startYear = startYear
        self.endYear = endYear
        self.stationCount = stationCount
    

@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        s1 = searchData(form.longitude.data,form.latitude.data,form.radius.data,form.startYear.data, form.endYear.data,form.stationCount.data)
        test = s1.radius
        return redirect(url_for('home'))
    else:
        #Standort Fürth
        form.latitude.data = 49.4771
        form.longitude.data = 10.9887

        #Standard-Werte
        form.radius.data = 50
        form.stationCount.data = 5
        form.startYear.data = 2000 #Keine Anforderung
        form.endYear.data = 2024 #Keine Anforderung
    
    return render_template('Startseite.html', form=form)

@app.route("/jahresansicht")
def jahresansicht():
    return render_template('Jahresansicht.html')

@app.route("/liste")
def liste():
    return render_template('Liste.html')

@app.route("/monatsansicht")
def monatsansicht():
    return render_template('Monatsansicht.html')

@app.route("/tagesansicht")
def tagesansicht():
    return render_template('Tagesansicht.html')


if __name__ == '__main__':
    app.run(debug=True)