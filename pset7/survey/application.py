import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("className") or not request.form.get("classLink"):
        return render_template("error.html", message="Please provide the correct data")
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["className", "classLink", "skillName", "classTech", "classImportant"])
        writer.writerow({"className": request.form.get("className"), "classLink": request.form.get("classLink"), "skillName": request.form.get("skillName"), "classTech": request.form.get("classTech"), "classImportant": request.form.get("classImportant")})
    return render_template("success.html", message=request.form.get("className"))


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # return render_template("error.html", message="You haven't registered any course yet")
    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        classes = list(reader)
    return render_template("sheet.html", classes=classes)
