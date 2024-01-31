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
        flash(f"Übermittelte Werte: {s1.latitude}, {s1.longitude}, {s1.radius}, {s1.startYear}, {s1.endYear}, {s1.stationCount}")
        return redirect(url_for('yearView'))
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
def yearView():
    form = searchForm(request.form)
    return render_template('Jahresansicht.html', form=form)

@app.route("/liste")
def liste():
    form = searchForm(request.form)
    return render_template('Liste.html',form=form)

@app.route("/monatsansicht")
def monthView():
    form = searchForm(request.form)
    return render_template('Monatsansicht.html', form=form)

@app.route("/tagesansicht")
def dayView():
    form = searchForm(request.form)
    return render_template('Tagesansicht.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)