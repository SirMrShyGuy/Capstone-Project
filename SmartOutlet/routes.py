from flask import render_template
from SmartOutlet import app
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#Outlet Info
outletInfo = [
    {"id": 0, "name": "Outlet 1", "pinNum": 5, "state": GPIO.LOW},
    {"id": 1, "name": "Outlet 2", "pinNum": 6, "state": GPIO.LOW},
    {"id": 2, "name": "Outlet 3", "pinNum": 13,"state": GPIO.LOW},
    {"id": 3, "name": "Outlet 4", "pinNum": 19,"state": GPIO.LOW}
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
