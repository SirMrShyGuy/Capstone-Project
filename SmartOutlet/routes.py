from flask import render_template, Response
from SmartOutlet import app
import RPi.GPIO as GPIO
import pygal
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Outlet Info
outletInfo = [
    {"id": 0, "name": "outlet1", "pinNum": 6, "state": GPIO.LOW},
    {"id": 1, "name": "outlet2", "pinNum": 13, "state": GPIO.LOW},
    {"id": 2, "name": "outlet3", "pinNum": 19,"state": GPIO.LOW},
    {"id": 3, "name": "outlet4", "pinNum": 26,"state": GPIO.LOW}
    ]

#Start GPIO setup
for pin in outletInfo:
    GPIO.setup(pin["pinNum"], GPIO.OUT)
    GPIO.output(pin["pinNum"], GPIO.LOW)

sqlite_file='/home/pi/Capstone-Project/Database/data_49002.sqlite'

def readDB(current_outlet):
    countlimit = 100
    conn=sqlite3.connect(sqlite_file)
    b=conn.cursor()
    b.execute('SELECT count({cn}) FROM {tn}' .\
              format(cn=current_outlet, tn='holder'))
    count=b.fetchone()[0]
    conn.row_factory = lambda cursor, row: row[0]
    c=conn.cursor()

    if count>countlimit:
        count = count-countlimit
        c.execute('SELECT ({cn}) FROM {tn} LIMIT 100 OFFSET {cnt}'.\
                  format(cn=current_outlet, tn='holder', cnt=count, cntlimit=countlimit))
        current_values=c.fetchall()
    else:
        c.execute('SELECT ({cn}) FROM {tn}'.\
                  format(cn=current_outlet, tn='holder'))
        current_values=c.fetchall()
    conn.commit()
    conn.close()
    return current_values

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
    values = readDB(outletInfo[int(outletId)]["name"])

    chart = pygal.Line(show_legend=False)
    chart.title = outletInfo[int(outletId)]["name"] + " Power Usage"
    chart.x_title = "Time"
    chart.y_title = "Watts"
    chart.add(outletInfo[int(outletId)]["name"], values)
    return Response(response=chart.render(), content_type="image/svg+xml")
