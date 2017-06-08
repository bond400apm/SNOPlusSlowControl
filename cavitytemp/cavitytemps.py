#This script uses the Digital Temperature Sensor installed in Noel's
#Directory to read out the string of temperature sensors in the SNO+
#Cavity.  These values are then sent to the SNO+ couchDB where slow
#control data is saved.
#Written by: Teal Pershing
#Last Updated: 03/20/2017

import subprocess
import lib.couchutils as cu
import lib.tempreader as tr
import lib.alarmposter as ap
import logging
import sys, traceback
import time

DEBUG = False

# --------- Logger configuration ----------- #
CLOG_FILENAME = '/home/uwslowcontrol/pi_db/log/cavitytemp.log' #logfile source

logging.basicConfig(filename=CLOG_FILENAME,level=logging.INFO, \
    format='%(asctime)s %(message)s')

#Define what we want our system exception hook to do at an
#uncaught exception
def UE_handler(exec_type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))
    logging.exception("Error type: " + str(exec_type))
    logging.exception("Traceback: " + str(traceback.format_tb(tb)))

#At an uncaught exception, run our handler
sys.excepthook = UE_handler

# ------- /Logger configuration --------- #

#Sends command to temp reader, returns raw read data
def getReading():
    timedelay = '1'
    numreads = '1'  #Set to zero to forever loop
    sport = '/dev/ttyUSB0' #Location of serial port
    comm = ['digitemp_DS9097U','-i','-a','-d',timedelay,
        '-n',numreads,'-s',sport]
    #This is deprecated!  But we're stuck at 2.6.6 so...
    tempreading = subprocess.Popen(comm, stdout=subprocess.PIPE).communicate()[0]
    return tempreading

#Save readings to text file for Noel
def WriteReadToLog(TempReader):
    SensorReads = reader.getSensorLines()
    if SensorReads is not None:
        f = open("TempReadings.log","a")
        f.write("\n")
        for sensorline in SensorReads:
            combinedline = " ".join(sensorline)
            if DEBUG == True:
                print("LINE WRITEN TO LOG: " + combinedline)
            f.write(combinedline + "\n")
        f.close()

   
# --------- END Logger configuration -------- #

if __name__ == "__main__":
    channeldb = None
    channeldb = cu.getChannelParameters(channeldb)
    AlarmControl = ap.AlarmPoster(channeldb,"temp_sensors")
    print("ENTERING WHILE LOOP")
    while True:
        #Update thresholds in case they were changed on webpage
        channeldb_last = channeldb
        channeldb = cu.getChannelParameters(channeldb_last)
        AlarmControl.setCurrentChanneldb(channeldb)
        rawread = getReading()
        rawread = rawread.splitlines()
        reader = tr.TempReader(rawread)
        time_now = int(time.time())
        reader.settime(time_now)
        reader.setunit("(C)")
        reader.parseTemps()
        if reader.hasrawvalues == False:
            logging.info("No values grabbed from sensor. Sensor" + \
                " may have been polled by another source at this time.")
            time.sleep(60)
            continue
        elif reader.parsed == False:
            #no values to parse, try again in a minute
            logging.info("No values parsed, trying again in 1 min.")
            time.sleep(60)
            continue
        else:
            #values parsed. check for values outside threshold and alarm
            AlarmControl.currentValues = reader.readingdict
            AlarmControl.postAlarms()
            WriteReadToLog(reader)
            #save the dictionary to couchDB
            cu.saveValuesToCT(reader.readingdict)
            time.sleep(360)

