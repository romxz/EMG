#importing libraries

import serial
import matplotlib.pyplot as plt
import time
import csv
import os
import random
import datetime
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

#getting serial data

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

#initializing variables

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
#test variables
#vallist = []        
#val_a = []
#val_b = []
#point = []

#initializing plot and time

plt.ion()
#plt.axis([0,10,0,10])
time1 = time.time()
time2 = time.time()


#main loop

#while True:
while time2 - time1 < 5:    
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            if index!=0:
                print(a)
            #if index%2 == 0:
            #    val_a.append(a[index])
            #elif index%2 == 1:
            #    print(val_b)
            #    val_b.append(a[index])
                
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y])
                plt.scatter(x,y)
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
with open('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + num + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in all_data:
        writer.writerow(i)



#with open('test1.csv', 'wb') as testfile:
    #csv_writer = csv.writer(testfile)
    