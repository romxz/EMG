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
clusters = 7
scale_left = -1
scale_right = 9
converted = False


print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']


"""following function converts a 3D list to another 3D one"""
def threeDconv(array): #array = 2D matrix (3 rows, N columns)
    new_list = [[],[],[]]
    for i in range(len(array[0])):
        a = float(array[0][i])
        b = float(array[1][i])
        c = float(array[2][i])  
        f = (np.sqrt(3.0)/2)*(a-b)
        g = (1/2)*(2*c-a-b)
        h = np.sqrt(a**2 + b**2 + c**2)
        s = np.sqrt(f**2 + g**2 + 1)
        x = (h/s)*f
        y = (h/s)*g
        new_list[0].append(x)
        new_list[1].append(y)
        new_list[2].append(h)
    return new_list

""" 4. initializing plot and time """

fig0 = plt.figure(0)
ax = plt.axes(projection = "3d")
ax.set_xlim(scale_left,scale_right)
ax.set_ylim(scale_left,scale_right)
ax.set_zlim(scale_left,scale_right)
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
                
                if converted:
                    
                    converted_xyz = threeDconv([[x],[y],[z]])
                    x = converted_xyz[0][0]
                    y = converted_xyz[1][0]
                    z = converted_xyz[2][0]
                if (x<scale_right and y<scale_right and z<scale_right and x>scale_left and y>scale_left and z>scale_left):
                    all_data.append([x,y,z])
                    ax.scatter(x,y,z, c='y', s=10, marker = "o")
                    #needs delay or else crashes
                    plt.pause(0.00000001)
                    time2 = time.time()
            index += 1
            line = []

    
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
    alldata, clusters, 2, error=0.0005, maxiter=10000, init=None, seed=None) 
cluster_membership = np.argmax(u, axis=0)
#print(cluster_membership)

""" 4. plotting the points according to membership + plotting centroids """

for j in range(clusters):              #change depending on number clusters
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i], marker = 'o', c = colors[j], s = 50)
    ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    
""" 5. adding line between centroids """

"""for point in cntr:
    for point2 in cntr:
        ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
"""        
""" 6. saving the figure as a png file """

plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\3Dfig' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\3Dfig' + num + '.png')

        
""" 7. resetting the plot with only centroids """

fig2 = plt.figure(2)
ax = plt.axes(projection = "3d")
ax.set_xlim(scale_left,scale_right)
ax.set_ylim(scale_left,scale_right)
ax.set_zlim(scale_left,scale_right)
for j in range(clusters):              #change value to match clusters
    ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)


fig1 = plt.figure(1)
ax = plt.axes(projection = "3d")
ax.set_xlim(scale_left,scale_right)
ax.set_ylim(scale_left,scale_right)
ax.set_zlim(scale_left,scale_right)
for j in range(clusters):              #change value to match clusters
    ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    

""" C. SECOND LOOP (RUNS INDEFINITELY) """

index = 0
while index<500:       #can change time (seconds)
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
                x = float(a[0])
                y = float(a[1])
                z = float(a[2])
                
                if converted:
                    converted_xyz = threeDconv([[x],[y],[z]])
                    x = converted_xyz[0][0]
                    y = converted_xyz[1][0]
                    z = converted_xyz[2][0]
                if (x<scale_right and y<scale_right and z<scale_right and x>scale_left and y>scale_left and z>scale_left):
                    a_array = np.asarray([[x], [y], [z]])
                    v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                    cluster_num = np.argmax(v[0], axis = 0)
                    cluster_num = int(cluster_num)
                    ax.set_xlim(scale_left,scale_right)
                    ax.set_ylim(scale_left,scale_right)
                    ax.set_zlim(scale_left,scale_right)
                    ax.scatter(x,y,z,s=40, c = colors[cluster_num])
                    plt.pause(0.000000001)
                    ax.clear()
                    ax.set_xlim(scale_left,scale_right)
                    ax.set_ylim(scale_left,scale_right)
                    ax.set_zlim(scale_left,scale_right)
                    fig1 = plt.figure(1)
                    ax = plt.axes(projection = "3d")
                    for j in range(clusters):            
                        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)

                    #time101 = time.time()
                    #print ("FPS:" + str(1/(time101-time100)))
                        
                
                #if index == 10:
                    #index = 0
                #index += 1
            line = []
    index+=1


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