import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import glob
import os

style.use('fivethirtyeight')
#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
plt.ion()
plt.show()

def animate(graph_data):
    #list_of_files = glob.glob('/Users/monicaburgers/Desktop/*.csv') # * means all if need specific format then *.csv
    #latest_file = max(list_of_files, key=os.path.getctime)
    #fileName = str(latest_file)

    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            print(x,y)
            xs.append(float(x))
            ys.append(float(y))
    #ax1.clear()
    #ax1.plot(xs, ys)
    #plt.clf()
    plt.scatter(xs,ys)
    plt.plot(xs, ys)
    plt.pause(0.0001)
    plt.draw()


#ani = animation.FuncAnimation(fig, animate, interval=1000)
#plt.show()

def main():
    graph_data = open('/Users/monicaburgers/Desktop/MIE491/MSEData_2.csv','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            print(x,y)
            xs.append(float(x))
            ys.append(float(y))
    #ax1.clear()
    #ax1.plot(xs, ys)
    #plt.clf()
    plt.scatter(xs,ys)
    plt.plot(xs, ys)
    plt.pause(0.0001)
    plt.draw()
    plt.xlabel("Displacement (mm)")
    plt.ylabel("Force (N)")

if __name__ == '__main__':
    while True:
        main()
