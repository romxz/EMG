"""
PLOTTING LIVE DATA AND ANALYSIS

use with arduino code "new3D"

features as of current iteration 
- live plotting
- clustering (fuzzy c)
- drawing lines between centroids
- continued plotting
"""

""" A. INITIALIZATION AND SETUP """

""" 1. importing the relevant libraries """

import serial
import matplotlib.pyplot as plt
import time
import csv
import random
import datetime
import numpy as np
import math
import skfuzzy as fuzz
import os
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

""" 2. retrieving serial data """

ser = serial.Serial(port='COM10',baudrate=9600,timeout=None)

""" 3. initializing starting variables """

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']

""" 4. initializing plot and time """

fig0 = plt.figure(0)
plt.ion()
#plt.axis([0.5,5,0.5,5])
time1 = time.time()
time2 = time.time()

""" B. INITIAL DATA COLLECTION AND ANALYSIS"""


""" 1. starting the loop """

index = 0
while time2 - time1 < 120:       #can change time (seconds)
    if index>=20:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c))
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            if ((len(a) == 2)):
                if (len(a[0])>=4 & len(a[1])>=4):
                    time100 = time.time()
                    x = float(a[0])
                    y = float(a[1])
                    all_data.append([x,y])
                
                    plt.scatter(x,y,s=10, color = "y")
                    plt.pause(0.000000001)
                        
                    time101 = time.time()
                    print ("FPS:" + str(1/(time101-time100)))
                        
        #index += 1
            line = []
    index += 1
    time2 = time.time()
    
""" 2. storing the data in csv file """

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

 

""" 3. setting up and running the fuzzy c means algorithm """

x_val = []
y_val = []
for i in all_data:
    x_val.append(i[0])
    y_val.append(i[1])
alldata = [x_val[1:len(x_val)], y_val[1:len(y_val)]]
x_val = alldata[0];
y_val = alldata[1];
alldata = np.asarray(alldata)

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 5, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)
#print(cluster_membership)

""" 4. plotting the points according to membership + plotting centroids """

for j in range(5):              #change depending on number clusters
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            plt.plot(x_val[i], y_val[i], '.', color = colors[j])
    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
    
""" 5. adding line between centroids """

"""for point in cntr:
    for point2 in cntr:
        plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")"""
        
""" 6. saving the figure as a png file """

plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')
        
        
""" 7. resetting the plot with only centroids """

fig1 = plt.figure(1)
for j in range(5):              #change value to match clusters
    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")

""" C. SECOND LOOP (RUNS INDEFINITELY) """


while time2 - time1 < 6:       #can change time (seconds)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c))
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            if ((len(a) == 2)):
                if (len(a[0])>=4 & len(a[1])>=4):
                    print(a)
                    #time100 = time.time()
                    x = float(a[0])
                    y = float(a[1])

                    a_array = np.asarray([[x], [y]])
                    v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                    cluster_num = np.argmax(v[0], axis = 0)
                    cluster_num = int(cluster_num)
                    print(a)
                    plt.scatter(x,y,s=40, color = "cluster_num")
                    plt.pause(0.000000001)
                    plt.clf()
                    #plt.remove()
                    #plt.axis([0,100,0,100])
                    for j in range(5):              #change value to match clusters
                        plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
                        
                        #time101 = time.time()
                        #print ("FPS:" + str(1/(time101-time100)))
                        
        #index += 1
            line = []


"""
while True:  
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        elif (c == 13):
            if index%3==0:
                a = ("".join(str(x) for x in line))
                a = a.replace("\n", ",")
                a = a.split(",")
                a = ([x for x in a if x])
                x = float(a[0])
                y = float(a[1])
                a_array = np.asarray([[x], [y]])
                v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                cluster_num = np.argmax(v[0], axis = 0)
                cluster_num = int(cluster_num)
                print(a)
                #all_data.append([x,y])
                plt.scatter(x,y,s=40, color = colors[cluster_num])
                plt.pause(0.00000001)
                time2 = time.time()
                plt.clf()
                #plt.remove()
                #plt.axis([0,100,0,100])
                for j in range(5):              #change value to match clusters
                    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
            line = []
            

        """
# """ 7. resetting the plot with only centroids """
# 
# #fig1 = plt.figure(0)
# plt.clf()
# for j in range(5):              #change value to match clusters
#     plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
# print("yo")
# 
# """ C. SECOND LOOP (RUNS INDEFINITELY) """
# 
# 
# index = 0 
# while True:  
#     ser.reset_input_buffer()
#     ser.reset_output_buffer()
#     for c in ser.readline():
#         if not(c == 13):
#             line.append(chr(c)) 
#         elif (c == 13):
#             a = ("".join(str(x) for x in line))
#             a = a.replace("\n", ",")
#             a = a.split(",")
#             a = ([x for x in a if x])
#                 
#             
#             if len(a) == 2:   
#                 x = float(a[0])
#                 y = float(a[1])
#                 all_data.append([x,y])
#                 plt.scatter(x,y,s=40, color = "k")
#                 plt.pause(0.00000001)
#                 time2 = time.time()
#                 plt.clf()
#                 #plt.remove()
#                 #plt.axis([0,100,0,100])
#                 for j in range(5):              #change value to match clusters
#                     plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
#             #index += 1
#         line = []
#             
#             
    
ser.close()
