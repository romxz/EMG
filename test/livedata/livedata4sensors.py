"""Plotting Live Data and Analysis of Data

use with arduino code "new3D"

features
- real-time plotting of up to 4 sensors
- automatic fuzzy c-means clustering
- lines between centroids
- continuous plotting with cluster predictions
"""


""" A. INITIALIZATION AND SETUP """


""" 1. importing relevant libraries """
import serial
import time
import datetime
import csv
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import skfuzzy as fuzz

os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

""" 2. retrieving serial data """

ser = serial.Serial(port = 'COM10', baudrate = 9600, timeout = None) #connected port
print ("connected to: " + ser.portstr)

""" 3. number of sensors """

num_sensors = int(input("Number of sensors: "))

""" 3. initializaing starting variables """
line = []
index = 0
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']

if num_sensors == 2:
    all_data = [["logrms1","logrms2"]]
    fig0 = plt.figure(0)
elif num_sensors == 3:
    all_data = [["logrms1","logrms2", "logrms3"]]
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")
elif num_sensors == 4:
    all_data = [["logrms1","logrms2", "logrms3", "logrms4"]]
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")

start_time = time.time()
end_time = time.time()


""" B. INITIAL DATA COLLECTION AND ANALYSIS """

""" 1. data collection loop """

while end_time - start_time < 120:    #time in seconds
    if index >= 20:                   #arbitrary choice
        ser.reset_input_buffer()
        ser.reset_output_buffer()
    for c in ser.readline():
        if not (c == 13):
            line.append(chr(c))
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            
            if num_sensors == 2:
                if ((len(a) == 2)):
                    if (len(a[0])>=4 & len(a[1])>=4):
                        x = float(a[0])
                        y = float(a[1])
                        all_data.append([x,y])
                        plt.scatter(x,y,s=10, color = "y")
                        plt.pause(0.00001)
            elif num_sensors == 3:
                if ((len(a) == 3)):
                    if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4):
                        x = float(a[0])
                        y = float(a[1])
                        z = float(a[2])
                        all_data.append([x,y,z])
                        ax.scatter(x,y,s=10, c = "y")
                        plt.pause(0.00001)
            elif num_sensors == 4:
                if ((len(a) == 4)):
                    if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4 & len(a[3])>=4):
                        x = float(a[0])
                        y = float(a[1])
                        z = float(a[2])
                        w = float(a[3])
                        all_data.append([x,y,z,w])
                        ##NOT SURE WHAT TO PLOT HERE YET
                        #ax.scatter(x,y,s=10, c = "y")
                        #plt.pause(0.00001)
        line = []
    index += 1
    end_time = time.time()
    
""" 2. storing data in csv file """

num1 = datetime.datetime.now().date() 
num2 = datetime.datetime.now().time() 
num =  num1.isoformat() + "..." + num2.isoformat()
num = (str(num).replace(":","-"))
num = (str(num).replace("-","."))

with open('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + num + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in all_data:
        writer.writerow(i)

print("file saved as: " + 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\test' + str(num) + '.csv')

""" 3. running the fuzzy c-means algorithm """

alldata = np.transpose(np.asarray(alldata[1:]))

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 5, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)

""" 4. plotting the points and centroids """

if num_sensors == 2:
    for j in range(5):      #change depending on number clusters
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                plt.scatter(alldata[0][i], alldata[1][i], color = colors[j], s= 20, marker = ".")
        plt.scatter(cntr[j][0], cntr[j][1], color = colors[j], s= 50, marker = "s")
elif (num_sensors == 3):
    for j in range(5):
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i],c = colors[j], s = 20, marker = ".")
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
##
# elif (num_sensors == 4):
#     for j in range(5):
#         for i in range(len(cluster_membership)):
#             if cluster_membership[i] == j:
#                 ~~~~
#     ~~~~

""" 5. adding line between centroids """

for point in cntr:
   for point2 in cntr:
       ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
       
""" 6. saving figure as a png file """
    
plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')

""" 7. resetting the plot with only centroids """

if num_sensors == 2:
    fig0 = plt.figure(0)
elif num_sensors == 3:
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")
elif num_sensors == 4:
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")

for j in range(5):              #change value to match clusters
    if num_sensors == 2:
        plt.scatter(cntr[j][0], cntr[j][1], c = colors[j], marker = "s", s = 50)
    elif num_sensors ==3:
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
        

""" C. CONTINUOUS REAL-TIME TRACKING """

while True:    
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    for c in ser.readline():
        if not (c == 13):
            line.append(chr(c))
        elif (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
            a = ([x for x in a if x])
            
            if num_sensors == 2:
                if ((len(a) == 2)):
                    if (len(a[0])>=4 & len(a[1])>=4):
                        x = float(a[0])
                        y = float(a[1])
        
                        a_array = np.asarray([[x], [y]])
                        v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                        cluster_num = int(np.argmax(v[0], axis = 0))
                        #print(a)
                        plt.scatter(x,y, s=40, color = colors[cluster_num])
                        plt.pause(0.000001)
                        plt.clf()
                        for j in range(5):    #change value to match clusters
                            plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
            elif num_sensors == 3:
                if ((len(a) == 3)):
                    if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4):
                        x = float(a[0])
                        y = float(a[1])
                        z = float(a[2])
                        a_array = np.asarray([[x], [y], [z]])
                        v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                        cluster_num = int(np.argmax(v[0], axis = 0))
                        #print(a)
                        ax.scatter(x,y,z, s=40, color = colors[cluster_num])
                        plt.pause(0.00001)
                        plt.clf()
                        for j in range(5):    #change value to match clusters
                            ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
            
            elif num_sensors == 4:
                if ((len(a) == 4)):
                    if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>=4 & len(a[3])>=4):
                        x = float(a[0])
                        y = float(a[1])
                        z = float(a[2])
                        w = float(a[3])
                        a_array = np.asarray([[x], [y], [z],[w]])
                        v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                        cluster_num = int(np.argmax(v[0], axis = 0))
                        #print(a)
                        ###NOT SURE WHAT TO PLOT HERE
                        #ax.scatter(x,y,z, s=40, color = colors[cluster_num])
                        #plt.pause(0.00001)
                        #plt.clf()
                        #for j in range(5):    #change value to match clusters
                        #ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
                        
        line = []

