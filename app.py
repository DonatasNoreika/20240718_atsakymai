from flask import Flask, render_template, request
from calendar import isleap

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run()