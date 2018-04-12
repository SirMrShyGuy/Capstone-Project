import sqlite3
import spidev
import time
import os
import RPi.GPIO as GPIO

sqlite_file='/home/pi/Desktop/Capstone-Project/Database/data_49002.sqlite'

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

outletInfo = [
    {"id": 0, "name": "outlet 1", "pinNum": 6, "state": GPIO.HIGH},
    {"id": 1, "name": "outlet 2", "pinNum": 13, "state": GPIO.HIGH},
    {"id": 2, "name": "outlet 3", "pinNum": 19,"state": GPIO.HIGH},
    {"id": 3, "name": "outlet 4", "pinNum": 26,"state": GPIO.HIGH}
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
        watts = [0]*4
        for i in range (4):
            lowValue = [512]*20
            highValue = [512]*20
            endOfTime = time.time() + 1
            while time.time() < endOfTime:
                value = readADC(i)
                if lowValue[i] > value:
                    lowValue[i] = value
                elif lowValue[i+4] > value:
                    lowValue[i+4] = value
                elif lowValue[i+8] > value:
                    lowValue[i+8] = value
                elif lowValue[i+12] > value:
                    lowValue[i+12] = value
                elif lowValue[i+16] > value:
                    lowValue[i+16] = value
                elif highValue[i] < value:
                    highValue[i] = value
                elif highValue[i+4] < value:
                    highValue[i+4] = value
                elif highValue[i+8] < value:
                    highValue[i+8] = value
                elif highValue[i+12] < value:
                    highValue[i+12] = value
                elif highValue[i+16] < value:
                    highValue[i+16] = value
		#Average of the remaining values after removing the highest and 5th highest values
                trueHigh = (highValue[i+4] + highValue[i+8] + highValue[i+12])/3
                trueLow = (lowValue[i+4] + lowValue[i+8] + lowValue[i+12])/3
                #voltage peak to peak times the adc reference voltage (5) and divided by 1024(max value)
                #vpp subtracted by 2.5 to get the actual value divided .1 for the volt to amp ratio then times wall voltage (120v)
                vpp = (trueHigh-trueLow)
                if GPIO.input(outletInfo[i]["pinNum"]) == False:
                    whatts = (vpp * 1.912)
                    if whatts > 0:
                        watts[i] = whatts
                    else:
                        watts[i] = 0
                else:
                    watts[i] = 0
        writeDB(watts)
        time.sleep(1)
    return

