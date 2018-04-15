import spidev
import time
import os
import sqlite3

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000


	# Write to database
def writeDB(watts[], table_name):
    conn=sqlite3.connect(sqlite_file)
    c=conn.cursor()
    c.execute("INSERT INTO {tn} ({cn1}, {cn2}, {cn3}, {cn4}) VALUES ("watts[1]", "watts[2]", "watts[3]", "watts[4])\"".\
              format(tn='holder', cn1='outlet1', cn2='outlet2', cn3='outlet3', cn4='outlet4'))
    conn.commit()
    conn.close
    return
	
	# func to read MCP3008 chip
def readADC(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data
	
	
	
	
	
	while True:
		VPP = [0]*4
		lowValue = [512]*4
		highValue = [512]*4
		watts = [0]*4
		endOfTime = 
		for i in range (4):
			endOfTime = time.time() + 1
			while time.time() < endOfTime:
				value = 512
				value = readADC[i]
			
				if lowValue[i] > value:
					lowValue[i] = value
				elif highValue[i] < value:
					highValue[i] = value
				#voltage peak to peak times the adc reference voltage (5) and divided by 1024(max value)
				#vpp subtracted by 2.5 to get the actual value times .1 for the volt to amp ratio then times wall voltage (120v)
				watts[i] = (highValue[i]-lowValue[i]) *2.92969
			
			
		writeDB(watts[])
		time.sleep(120)
			
	
	
	
	
	
	
	