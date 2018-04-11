#!/usr/bin/env python
import sys
sys.path.append('/home/pi/Desktop/GrovePi/Software/Python/')
import time
import datetime
from grovepi import *
import serial

# for GPS
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0) #Open the serial port at 9600 baud
ser.flush()

class GPS:
        inp=[]
        GGA=[]
        def read(self):
                while True:
                        GPS.inp=ser.readline()
                        if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
                                break
                        time.sleep(0.1)
                try:
                        ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))
                        GPS.inp=GPS.inp[ind:]
                except ValueError:
                        print "error"
                GPS.GGA=GPS.inp.split(",")
                return [GPS.GGA]

        def vals(self):
                time=GPS.GGA[1]
                lat=GPS.GGA[2]
                lat_ns=GPS.GGA[3]
                long=GPS.GGA[4]
                long_ew=GPS.GGA[5]
                fix=GPS.GGA[6]
                sats=GPS.GGA[7]
                alt=GPS.GGA[9]
                return [time,fix,sats,alt,lat,lat_ns,long,long_ew]

# for Japan Timestamp
class JapanTZ(datetime.tzinfo):
    def tzname(self, dt):
        return "JST"
    def utcoffset(self, dt):
        return datetime.timedelta(hours=9)
    def dst(self, dt):
        return datetime.timedelta(0)


ptemperature = 3
pmoisture = 0
plight = 1

pinMode(ptemperature,"INPUT")
pinMode(pmoisture,"INPUT")
pinMode(plight,"INPUT")
time.sleep(1)

[temperature, humidity] = dht(ptemperature, 1)
moisture = analogRead(pmoisture)

light = analogRead(plight)

print("{0},{1},{2},{3},{4}".format(datetime.datetime.now(JapanTZ()).strftime('%Y-%m-%dT%H:%M:%S+09:00'), temperature, humidity, moisture, light))

ser.close()
