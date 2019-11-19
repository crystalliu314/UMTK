import serial
from time import sleep

BAUD_RATE = 9600
PORT = "COM3"
REFRESH_RATE = 0.05 # How often the graph refreshes, in seconds

ser = serial.Serial(timeout = 0.5)
ser.baud_rate = BAUD_RATE
ser.port = PORT

ser.open()
print("opened")
#sleep(0.5)

i = 0
data = []
while True:
    temp = (ser.readline().decode()).strip()
    if temp != '':
        data.append(temp)

    print(temp)
    #sleep(0.5)
    i += 1

ser.close()
