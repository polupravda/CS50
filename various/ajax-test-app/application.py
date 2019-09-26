import cs50
from flask import Flask, render_template, request

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fundament")
def fundament():
    return render_template("fundament.html")