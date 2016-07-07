#use with arduino code "new"

#importing libraries

import serial
import matplotlib.pyplot as plt

import time
import csv
import os
import random
import datetime
import numpy as np
import math
import skfuzzy as fuzz
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

#getting serial data

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

#initializing variables

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']
#test variables
#vallist = []        
#val_a = []
#val_b = []
#point = []

#initializing plot and time

plt.ion()
plt.axis([0.5,5,0.5,5])

time1 = time.time()
time2 = time.time()
#MAIN LOOP

#time3 = 0
#time4 = 0

#while True:
#can change time below (seconds)
while time2 - time1 < 200:
    
    #time1 = time.time()
    #a = time.time()
       
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c))
        
            #b = time.time()
        
        elif (c == 13):
            
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            print(a)
            #c = time.time()
            #time2 = (c-b)
            
            
            if index%4==0:
            #if index!=0:
                
                time100 = time.time()
                #print(a)
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y])
                
                #d = time.time()
                #time3 = (d-c)
                
                plt.scatter(x,y,s=10, color = "y")
                plt.pause(0.000000001)
                
                #e = time.time()
                #time4 = (e-d)
                
                #time101 = time.time()
                #print ("FPS:" + str(1/(time101-time100)))
                    
            index += 1
            line = []
    
    time2 = time.time()
    
    #max_value = max([time2,time3,time4])
    #max_index = [time2,time3,time4].index(max_value)
    #print(max_index)
    
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

print("file saved as: " + 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + str(num) + '.csv')

#make a nested array, each index being an array of log rms (length = # of trials)

x_val = []
y_val = []
for i in all_data:
    x_val.append(i[0])
    y_val.append(i[1])
alldata = [x_val[2:len(x_val)], y_val[2:len(y_val)]]
x_val = alldata[0];
y_val = alldata[1];
alldata = np.asarray(alldata)
#print(alldata)

#running fuzzy c-means algorithm (second num is # clusters)

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 5, 2, error=0.0005, maxiter=10000, init=None, seed=None)
cluster_membership = np.argmax(u, axis=0)
print(cluster_membership)
#change depending on number clusters
for j in range(5):
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            plt.plot(x_val[i], y_val[i], '.', color = colors[j])
    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")

#adding line between centroids

"""for point in cntr:
    for point2 in cntr:
        plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")"""

#SECONDARY LOOP
#continuing after saved file (indefinitely atm)

"""
while True:  
    n=4
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            if index%n==0:
                print(a)
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y])
                plt.scatter(x,y,s=40, color = "k")
                plt.pause(0.00000001)
                time2 = time.time()
            index += 1
            line = []
    n = int(n+index/100)

"""    
