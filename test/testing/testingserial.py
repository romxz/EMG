""" A. INITIALIZATION AND SETUP """

""" 1. importing the relevant libraries """

import serial

""" 2. retrieving serial data """

ser = serial.Serial(port='COM10',baudrate=1200)

""" 3. initializing starting variables """

print("connected to: " + ser.portstr)

line = []           #storing the numbers until it reaches a space

while True:       #can change time (seconds)
    c = ser.readline()
    c = str(c[0:-2])
    c = c[2:-1]
    c = [float(x.strip()) for x in c.split(',')]
    print(c)
    print(type(c[0]))