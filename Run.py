#!/usr/bin/python

#Import Libraries
import os.path
import datetime
import time
import sys
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#Setup for Serial Communication with Arduino (Using USB Cable)
arduinoSerial = serial.Serial('/dev/cu.usbmodem14201',9600)
#plt.ion()

def animateGraph(file):
    style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        graph_data = open(file,'r').read()
        lines = graph_data.split('\n')
        lines.pop(0)
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(float(x))
                ys.append(float(y))
        ax1.clear()
        ax1.plot(xs, ys)

    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()

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

                #Initialize Graph
                style.use('fivethirtyeight')
                fig = plt.figure()
                ax1 = fig.add_subplot(1,1,1)

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
                    datasheetFile.close()

                    animateGraph(completeFileNameAndPath)

                    graph_data = open(completeFileNameAndPath,'r').read()
                    lines = graph_data.split('\n')
                    lines.pop(0)
                    xs = []
                    ys = []
                    for line in lines:
                        if len(line) > 1:
                            x, y = line.split(',')
                            xs.append(float(x))
                            ys.append(float(y))
                    plt.grid(True)
                    plt.ylabel("Scale Reading")
                    plt.xlabel("Displacement")
                    plt.plot(xs, ys)
                    plt.pause(0.000001)

                    datasheetFile = open(completeFileNameAndPath, "a")
    #---LOOP---

if __name__ == '__main__':
    main()
