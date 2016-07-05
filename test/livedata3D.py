#importing libraries

import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
#fig = plt.figure()
#ax = plt.axes(projection='3d')
import time
import random
import csv
import os
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")
import numpy as np
import skfuzzy as fuzz
import datetime

#getting serial data

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

#initializing variables

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2","logrms3"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']
#test variables
#vallist = []        
#val_a = []
#val_b = []
#point = []

#initializing plot and time

plt.ion()
time1 = time.time()
time2 = time.time()


#MAIN LOOP

#while True:
while time2 - time1 < 120:    
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
                all_data.append([x,y,z])
                print([x,y,z])
                ax.scatter(x,y,z, c='y', s=10, marker = "o")
                #ax.plot(x,y,z,'-b')
                #needs delay or else crashes
                plt.pause(0.00000001)
                
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

print("file saved as: " + 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + str(num) + '.csv')


#make a nested list, first list is x values seperated by double space, second list is y values
x_val = []
y_val = []
z_val = []
for i in all_data:
    x_val.append(i[0])
    y_val.append(i[1])
    z_val.append(i[2])
alldata = [x_val[2:len(x_val)], y_val[2:len(y_val)], z_val[2:len(z_val)]] #don't want the titles
x_val = alldata[0];
y_val = alldata[1];
z_val = alldata[2];
alldata = np.asarray(alldata)
#print(alldata)

#running fuzzy c-means algorithm (second num is # clusters)
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 4, 2, error=0.0005, maxiter=10000, init=None, seed=None)
cluster_membership = np.argmax(u, axis=0)
print(cluster_membership)
#change depending on number clusters
for j in range(4):
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax.scatter(x_val[i], y_val[i], z_val[i], c = colors[j],s = 20, marker = "o")
    ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)


#SECONDARY LOOP
#continuing on after data has been saved (indefinitely atm)

while True:    
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
                print([x,y,z])
                all_data.append([x,y,z])
                ax.scatter(x,y,z, c='y', s=10, marker = "o")
                #needs delay or else crashes
                plt.pause(0.00000001)
                
                time2 = time.time()
            
            index += 1
            line = []