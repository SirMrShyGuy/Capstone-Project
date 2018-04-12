import spidev
import time
import os
import sqlite3

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

#sqlite data
table_name='holder'

# func to read MCP3008 chip
def readADC(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# convert data to volts
def convertToVolts(data, rounding):
    volts = (data * 5) / float(1023)
    volts = round(volts, rounding)
    return volts

def convertToMilVolts(data, rounding):
    milVolts = (data / 1024.0) * 5000.0
    milVolts = round(milVolts, rounding)
    return milVolts

def voltsToCurrent(volt, rounding):
    current = ((volt - 2500.0) / 66.0)
    current = round(current, rounding)
    return current

# sample test
if __name__ == "__main__":
    print("Reading MCP3008 values channels 0 to 7 (ctrl-c to quit)")
    # header
    #print("| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4}".format(*range(8)))

    while True:
        #store values in a list
        values = [0]*8
        volts = [0]*8
        milVolts = [0]*8
        current = [0]*8
        for i in range(8):
            values[i] = readADC(i)
            volts[i] = convertToVolts(values[i], 2)
            milVolts[i] = convertToMilVolts(values[i], 2)
            current[i] = voltsToCurrent(milVolts[i], 2)
#        print("| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | raw data".format(*values))
#        print("| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | volts".format(*volts))
        print(values[0], " : ", volts[0], " : ", milVolts[0], " : ", current[0])
        time.sleep(.1)
