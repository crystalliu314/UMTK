#!/usr/bin/python

#Import Libraries
import os.path
import datetime
import time
import sys
import serial
import matplotlib.pyplot as plt
from matplotlib import style

#Setup for Serial Communication with Arduino (Using USB Cable)
arduinoSerial = serial.Serial('/dev/cu.usbmodem14101',9600)

#Specify directory to save files to
directory = "/Users/monicaburgers/Desktop/"

#Initilaize variables to store incoming data
xdata = []
ydata = []

def graph(currentSerialLine):
    #This function takes the input of a single line of data rom the Arduino and
    # adds it to the graph. It assumes there are only 2 numbers, separated by a
    # comma.

    x, y = currentSerialLine.split(', ') #Split the incoming string into 2 numbers
    ydata.append(float(y)) #Convert strings to numbers
    xdata.append(float(x))

    #plt.suptitle("") #Add title to graph
    plt.xlabel("Displacement (mm)") #Add axis labels
    plt.pause(0.0001)
    plt.ylabel("Scale Reading (kg)")
    plt.pause(0.0001)

    plt.plot(xdata,ydata, 'b') #Add the new data point to the plot
    plt.pause(0.0001)
    plt.draw() #Redraw the graph window
    plt.pause(0.0001)

def main():
    #---SETUP---
    record = False #Don't record incoming data until the test is ready to be run

    plt.ion() #Turn on interactive mode for graph
    plt.pause(0.0001)
    plt.show() #Display the graph
    plt.pause(0.0001)
    plt.clf() #Clear the graph
    plt.pause(0.0001)

    fileString = raw_input('Enter name of data file: ') #Get user to input desired nme of the file to save data to

    #print "Press button to start recording data."
    #---SETUP---

    #---LOOP---
    while True:
        #Waits for Arduino to send data through Serial
        if arduinoSerial.inWaiting():
            #Reads single line from serial
            currentSerialLine = arduinoSerial.readline()

            #If 'Start' button pressed
            if currentSerialLine == "BEGIN\n":
                record = True #Start recording data
                print "Starting Test"

                #Create file to save data to within specified directory
                fileName = str(fileString) + '.csv'
                completeFileNameAndPath = os.path.join(directory, fileName)
                datasheetFile = open(completeFileNameAndPath, "a")

                #Add a header label to the .csv file
                header = "Displacement (mm), Scale Reading (kg) \n"
                datasheetFile.write(header)
                print header

            elif record == True:
                #If 'End' button pressed
                if currentSerialLine == "END\n":
                    print "Ending Test"
                    record = False

                    #Save image of the graph to specified directory
                    imageFileName = str(fileString) + '.png'
                    imageFilePath = os.path.join(directory, imageFileName)
                    plt.savefig(imageFilePath)

                    #Close the data file
                    datasheetFile.close()

                    #Ask if another test is going to be run
                    while True:
                        answer = raw_input('Run another test? (y/n): ')
                        if answer in ('y', 'n'):
                            break
                        print 'Invalid input.'
                    if answer == 'y':
                        #If another test is being run, restart the script
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    else:
                        #If testing is done, close the script
                        print 'Goodbye'
                        break
                else:
                    print currentSerialLine
                    datasheetFile.write(currentSerialLine) #Write new line of data to file
                    graph(currentSerialLine) #Graph the new data point

    #---LOOP---

if __name__ == '__main__':
    main()
