from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route("/")
def home():
    return render_template('Startseite.html')

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