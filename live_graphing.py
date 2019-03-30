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
import pandas

#Setup for Serial Communication with Arduino (Using USB Cable)
arduinoSerial = serial.Serial('/dev/cu.usbmodem14101',9600)
xdata = []
ydata = []
#figNum = 0

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

def makeFig(number):
    figure = plt.figure(number)
    plt.ion()
    plt.pause(0.0001)
    plt.show()
    plt.pause(0.0001)
    plt.cla()
    plt.pause(0.0001)
    plt.clf()
    plt.pause(0.0001)
    plt.close(figure)
    plt.pause(0.0001)
    return figure

def graph(currentSerialLine):
    x, y = currentSerialLine.split(', ')
    ydata.append(float(y))
    xdata.append(float(x))
    plt.plot(xdata,ydata, 'b')
    plt.pause(0.0001)
    plt.draw()
    plt.pause(0.0001)

def main():
    #---SETUP---
    record = False
    xdata = []
    ydata = []
    #if(figNum > 0):
        #plt.close(figNum - 1)
    #fig = makeFig(figNum)

    plt.ion()
    plt.pause(0.0001)
    plt.show()
    plt.pause(0.0001)
    plt.cla()
    plt.pause(0.0001)
    plt.clf()
    plt.pause(0.0001)

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
                    #figNum += 1
                    #main()
                    while True:
                        answer = raw_input('Run another test? (y/n): ')
                        if answer in ('y', 'n'):
                            break
                        print 'Invalid input.'
                    if answer == 'y':
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    else:
                        print 'Goodbye'
                        break
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
