#!/usr/bin/python

#Import Libraries
import os.path
import datetime
import time
import sys
import serial
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import Image

#Setup for Serial Communication with Arduino (Using USB Cable)
arduinoSerial = serial.Serial('/dev/cu.usbmodem14101',9600)
xdata = []
ydata = []
#style.use('fivethirtyeight')
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)


def animate(i):
    list_of_files = glob.glob('/Users/monicaburgers/Desktop/*.csv') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    fileName = str(latest_file)

    graph_data = open(fileName,'r').read()
    lines = graph_data.split('\n')
    lines.pop(0)
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(', ')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)

def animateGraph(file):
    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()

def graph(currentSerialLine):
    x, y = currentSerialLine.split(', ')
    ydata.append(float(y))
    xdata.append(float(x))
    plt.clf()
    plt.scatter(xdata,ydata)
    plt.plot(xdata, ydata)
    plt.pause(0.0001)
    plt.draw()

def main():
    #---SETUP---
    record = False
    xdata = []
    ydata = []
    plt.ion()
    plt.show()
    
    print(xdata)
    
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

                header = "Displacement (mm), Scale Reading (kg)"
                datasheetFile.write(header)
                print header

            elif record == True:
                if currentSerialLine == "END\n":
                    print "Ending Test"
                    record = False
                    datasheetFile.close()
                    #plt.clf()
                    #plt.cla()
                    plt.pause(0.0001)
                    plt.close()
                    main()
                else:
                    print currentSerialLine
                    datasheetFile.write(currentSerialLine)
                    #datasheetFile.close()

                    #animateGraph(completeFileNameAndPath)
                    #plt.close()

                    graph(currentSerialLine)

                    #datasheetFile = open(completeFileNameAndPath, "a")
    #---LOOP---

if __name__ == '__main__':
    main()
