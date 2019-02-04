#!/usr/bin/python

#Import Libraries
import os.path
import datetime
import time
import sys
import serial

#Setup for Serial Communication with Arduino (Using USB Cable)
arduinoSerial = serial.Serial('/dev/cu.usbmodem14201',9600)

def main():
    #---SETUP---
    record = False
    print "Press button to start recording data."
    #---SETUP---
    
    #---LOOP---
    while True:
        #Waits for Arduino to send data through Serial
        if arduinoSerial.inWaiting():
            #Reads single line from serial
            currentSerialLine = arduinoSerial.readline()
            
            if currentSerialLine == "BEGIN\n":
                record = True
                print "Starting Test"
                #Initializing File Name to Current Date and File Path
                currentDate = datetime.datetime.now()
                fileName = str(currentDate) + '.csv'
                completeFileNameAndPath = os.path.join("/Users/monicaburgers/Desktop/", fileName)
                datasheetFile = open(completeFileNameAndPath, "a")

                print "Displacement (mm), Scale Reading (kg)"
                header = "Displacement (mm), Scale Reading (kg)"
                datasheetFile.write(header)
            
            if record == True:
                if currentSerialLine == "END\n":
                    print "Ending Test"
                    datasheetFile.close()
                    main()
                else:
                    print currentSerialLine
                    datasheetFile.write(currentSerialLine)
    #---LOOP---

if __name__ == '__main__':
    main()
