from flask import render_template, Response
from SmartOutlet import app
import RPi.GPIO as GPIO
import pygal
import sqlite3

GPIO.setmode(GPIO.BCM)

#Outlet Info
outletInfo = [
    {"id": 0, "name": "Outlet1", "pinNum": 5, "state": GPIO.LOW},
    {"id": 1, "name": "Outlet2", "pinNum": 6, "state": GPIO.LOW},
    {"id": 2, "name": "Outlet3", "pinNum": 13,"state": GPIO.LOW},
    {"id": 3, "name": "Outlet4", "pinNum": 19,"state": GPIO.LOW}
    ]

#Start GPIO setup
for pin in outletInfo:
    GPIO.setup(pin["pinNum"], GPIO.OUT)
    GPIO.output(pin["pinNum"], GPIO.LOW)

#-Home page 
@app.route("/")
@app.route("/index")
def index():
    templateData = {
            "title": "Home Page",
            "header": "Control Page",
            'outletInfo': outletInfo
            }
    return render_template("index.html", **templateData)

#-about page
@app.route("/about")
def about():
    return render_template("about.html", title="About Page", header="About Page")

#-changes state of selected outlet
@app.route("/<outletId>/<action>")
def action(outletId, action):
    #
    if action == "on":
        GPIO.output(outletInfo[int(outletId)]["pinNum"],GPIO.HIGH)
        outletInfo[int(outletId)]["state"]=GPIO.HIGH
    if action == "off":
        GPIO.output(outletInfo[int(outletId)]["pinNum"],GPIO.LOW)
        outletInfo[int(outletId)]["state"]=GPIO.LOW
    
    templateData = {
            "title": "Home Page",
            "header": "Control Page",
            'outletInfo': outletInfo
            }
    return render_template("index.html", **templateData)

#-creates images for graphs
@app.route("/<outletId>/graph")
def graph(outletId):
    chart = pygal.Line()
    chart.title = outletInfo[int(outletId)]["name"] + " Power Usage"
    chart.add(outletInfo[int(outletId)]["name"], [1,2,3,4,5,6,7,8,9,10])
    return Response(response=chart.render(), content_type="image/svg+xml")
