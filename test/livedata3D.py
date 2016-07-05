#importing libraries

import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = plt.axes(projection='3d')
import time
import random
import csv
import os
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")
import datetime

#getting serial data

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

#initializing variables

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2","logrms3"]]
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
while time2 - time1 < 3:    
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            print(a)
            if index!=0:
                x = float(a[0])
                y = float(a[1])
                #z needs to be initialized to something (probably a[2] but needs testing)
                z = random.randint(0,10)
                all_data.append([x,y,z])
                ax.scatter(x,y,z)
                #needs delay or else crashes
                plt.pause(0.0001)
                
                time2 = time.time()
            
            index += 1
            line = []

#filename is the time
num1 = datetime.datetime.now().date() 
num2 = datetime.datetime.now().time() 
num =  num1.isoformat() + "..." + num2.isoformat()
num = (str(num).replace(":","-"))
num = (str(num).replace("-","."))

#change save location below
with open('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + str(num) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in all_data:
        writer.writerow(i)
