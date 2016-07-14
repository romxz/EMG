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
from mpl_toolkits.mplot3d import Axes3D
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
record_time = 5
clusters = 4

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']

""" 4. initializing plot and time """

fig1 = plt.figure(figsize = (24,8))
ax1 = fig1.add_subplot(1, 2, 1, projection="3d")
ax2 = fig1.add_subplot(1, 2, 2, projection='3d')
ax1.set_xlim(-5,25)
ax1.set_ylim(-5,25)
ax1.set_zlim(-5,25)
ax2.set_xlim(-5,25)
ax2.set_ylim(-5,25)
ax2.set_zlim(-5,25)
plt.ion()
#plt.axis([0.5,5,0.5,5])
time1 = time.time()
time2 = time.time()

""" B. INITIAL DATA COLLECTION AND ANALYSIS"""


""" 1. starting the loop """

while time2 - time1 < record_time:  
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
            print(a)
            if ((len(a)==3)):
                   
                print(a)
                x = float(a[0])
                y = float(a[1])
                #z needs to be initialized to something (probably a[2] but needs testing)
                #z = random.randint(0,10)
                z = float(a[2])
                all_data.append([x,y,z])
                ax1.scatter(x,y,z, c='y', s=10, marker = "o")
                #needs delay or else crashes
                plt.pause(0.00000001)
                time2 = time.time()
            index += 1
            line = []

# index = 0
# while time2 - time1 < 120:       #can change time (seconds)
#     if index>=20:
#         ser.reset_input_buffer()
#         ser.reset_output_buffer()
#     for c in ser.readline():
#         if not(c == 13):
#             line.append(chr(c))
#         elif (c == 13):
#             a = ("".join(str(x) for x in line))
#             a = a.replace("\n", ",")
#             a = a.split(",")
#             a = ([x for x in a if x])
#             if ((len(a) == 3)):
#                 if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>4):
#                     x = float(a[0])
#                     y = float(a[1])
#                     #z needs to be initialized to something (probably a[2] but needs testing)
#                     #z = random.randint(0,10)
#                     z = float(a[2])
#                     all_data.append([x,y,z])
#                     print([x,y,z])
#                     ax.scatter(x,y,z, c='y', s=10, marker = "o")
#                     #needs delay or else crashes
#                     plt.pause(0.01)
#                     time2 = time.time()
#                         
#         #index += 1
#             line = []
#     index += 1
#     time2 = time.time()
    
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

alldata = np.transpose(np.asarray(all_data[1:]))

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, clusters, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)
#print(cluster_membership)

""" 4. plotting the points according to membership + plotting centroids """

for j in range(clusters):              #change depending on number clusters
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax1.scatter(alldata[0][i], alldata[1][i], alldata[2][i], marker = 'o', c = colors[j], s = 50)
    ax1.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    
""" 5. adding line between centroids """

"""for point in cntr:
    for point2 in cntr:
        ax.plot([point[0], point2[0]], [point[1], point2[1], [point[2],[point2[2]],"-b")"""
        
""" 6. saving the figure as a png file """

plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')
        
        
""" 7. resetting the plot with only centroids """

print("hi")
for j in range(clusters):              #change value to match clusters
    ax2.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)

""" C. SECOND LOOP (RUNS INDEFINITELY) """

index = 0
while True:       #can change time (seconds)
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
            if ((len(a) == 3)):
                #time100 = time.time()
                x = float(a[0])
                y = float(a[1])
                z = float(a[2])
                a_array = np.asarray([[x], [y], [z]])
                v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                cluster_num = np.argmax(v[0], axis = 0)
                cluster_num = int(cluster_num)
                ax2.scatter(x,y,z,s=40, c = colors[cluster_num])
                plt.pause(0.000000001)
                #if index>=10:
                ax1.set_xlim(-5,25)
                ax1.set_ylim(-5,25)
                ax1.set_zlim(-5,25)
                ax2.set_xlim(-5,25)
                ax2.set_ylim(-5,25)
                ax2.set_zlim(-5,25)
                ax2.clear()
                #ax2 = plt.axes(projection = "3d")
                #plt.remove()
                #plt.axis([0,100,0,100])
                for j in range(clusters):              #change value to match clusters
                    ax1.set_xlim(-5,25)
                    ax1.set_ylim(-5,25)
                    ax1.set_zlim(-5,25)
                    ax2.set_xlim(-5,25)
                    ax2.set_ylim(-5,25)
                    ax2.set_zlim(-5,25)
                    ax2.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)

                    #time101 = time.time()
                    #print ("FPS:" + str(1/(time101-time100)))
                        
                
                #if index == 10:
                    #index = 0
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