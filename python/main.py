from flask import Flask, render_template, request, flash, redirect, url_for
from forms import searchForm
import secrets

foo = secrets.token_urlsafe(16)



app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = foo

class searchData:
    def __init__(self,longitude,latitude,valueRange,startYear,endYear,stationCount):
        self.longitude = longitude
        self.latitude = latitude
        self.valueRange = valueRange
        self.startYear = startYear
        self.endYear = endYear
        self.stationCount = stationCount
    

@app.route("/", methods=['GET', 'POST'])
def home():
    form = searchForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        s1 = searchData(form.longitude,form.latitude,form.valueRange,form.startYear, form.endYear,form.stationCount)
        flash(s1.longitude)
        return redirect(url_for('home'))
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