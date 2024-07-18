from flask import Flask, render_template, request
from calendar import isleap
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# nustatėme, kad mūsų duomenų bazė bus šalia šio failo esants data.sqlite failas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# neseksime kiekvienos modifikacijos
db = SQLAlchemy(app)


# sukuriame duomenų bazės objektą
# sukurkime modelį užklausos formai, kuris sukurs duomenų bazėje lentelę


class Record(db.Model):
    # DB lentelei priskiria pavadinimą, jei nenurodysite, priskirs automatiškai pagal klasės pavadinimą.
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)  # stulpelis, kurio reikšmės integer. Taip pat jis bus primary_key.
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

    def __repr__(self):
        return f'{self.type}: {self.amount}'


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/zodziai/<zodis>")
def zodziai(zodis):
    return render_template("zodziai.html", zodis=zodis)


@app.route("/keliamieji")
def keliamieji():
    return render_template("keliamieji.html", isleap=isleap)


@app.route("/arkeliamieji", methods=["GET", "POST"])
def ar_keliamieji():
    if request.method == "POST":
        metai = int(request.form['metai'])
        keliamieji_bool = isleap(metai)
        return render_template("ar_keliamieji_result.html", ar_keliamieji_bool=keliamieji_bool, metai=metai)

    return render_template("ar_keliamieji.html")


@app.route("/biudzetas", methods=["GET", "POST"])
def biudzetas():
    if request.method == "POST":
        amount = request.form['amount']
        type = request.form['type']
        record = Record(amount, type)
        db.session.add(record)
        db.session.commit()
    zurnalas = Record.query.all()

    total = 0
    for irasas in zurnalas:
        if irasas.type == "Pajamos":
            total += irasas.amount
        if irasas.type == "Išlaidos":
            total -= irasas.amount
    return render_template("biudzetas.html", zurnalas=zurnalas, balansas=total)


if __name__ == "__main__":
    app.run()
