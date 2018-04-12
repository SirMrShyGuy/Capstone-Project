import sqlite3
import spidev
import time
import os
import RPi.GPIO as GPIO

sqlite_file='/home/pi/Desktop/data_49002.sqlite'

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

outletInfo = [
    {"id": 0, "name": "outlet1", "pinNum": 5, "state": GPIO.LOW},
    {"id": 1, "name": "outlet2", "pinNum": 6, "state": GPIO.LOW},
    {"id": 2, "name": "outlet3", "pinNum": 13,"state": GPIO.LOW},
    {"id": 3, "name": "outlet4", "pinNum": 19,"state": GPIO.LOW}
    ]

# Write to database
def writeDB(watts):
    conn=sqlite3.connect(sqlite_file)
    c=conn.cursor()
    c.execute('''INSERT INTO holder (outlet1, outlet2, outlet3, outlet4) VALUES (?,?,?,?)''', (watts[0], watts[1], watts[2], watts[3]))
    conn.commit()
    conn.close
    return

# func to read MCP3008 chip
def readADC(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Starts database collection
def run(): 
    while True:
        VPP = [0]*4
        lowValue = [512]*4
        highValue = [512]*4
        watts = [0]*4
        for i in range (4):
            endOfTime = time.time() + 1
            while time.time() < endOfTime:
                value = 512
                value = readADC(i)
                if lowValue[i] > value:
                    lowValue[i] = value
                elif highValue[i] < value:
                    highValue[i] = value
                #voltage peak to peak times the adc reference voltage (5) and divided by 1024(max value)
                #vpp subtracted by 2.5 to get the actual value times .1 for the volt to amp ratio then times wall voltage (120v)
                if GPIO.input(outletInfo[i]["pinNum"]) == True:
                    watts[i] = (highValue[i]-lowValue[i]) *2.92969
                else:
                    watts[i] = 0
        writeDB(watts)
        time.sleep(1)
    return

