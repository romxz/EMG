#importing libraries

import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = plt.axes(projection='3d')
import time
import random

#getting serial data

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

#initializing variables

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
#test variables
#vallist = []        
#val_a = []
#val_b = []
#point = []

#initializing plot and time

plt.ion()
time1 = time.time()
time2 = time.time()


#main loop

#while True:
while time2 - time1 < 300:    
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            if index!=0:
                x = float(a[0])
                y = float(a[1])
                #z needs to be initialized to something (probably a[2] but needs testing)
                z = random.randint(0,10)
                
                ax.scatter(x,y,z)
                #needs delay or else crashes
                plt.pause(0.0001)
                
                time2 = time.time()
            
            index += 1
            line = []
