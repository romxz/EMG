"""
PLOTTING LIVE DATA AND ANALYSIS

use with arduino code "new3D"

features as of current iteration 
- live plotting
- clustering (fuzzy c)
- drawing lines between centroids
- continued plotting
"""

""" Z. FUNCTIONS """

""" 1. Distance """
def distance(x,y): #2 same size horizontal lists
    sum = 0
    for i in range(0,len(x)):
        sum += np.abs((y[i] - x[i])**2)
        print(sum)
    return np.sqrt(sum)
    

""" A. INITIALIZATION AND SETUP """

""" 0. OPTIONS """
distance_limit = False #graph only if consecutive points exceed specific distance 
epsilon = 0.000001

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

time_run = 105
clusters = 7
left = 1
right = 9

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrmsx1","logrmsy1","logrmsx2","logrmsy2"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k']

""" 4. initializing plot and time """

fig1, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize = (16,8))
ax1.axis([left,right,left,right])
ax2.axis([left,right,left,right])
plt.ion()
#plt.axis([0.5,5,0.5,5])
time1 = time.time()
time2 = time.time()

""" B. INITIAL DATA COLLECTION AND ANALYSIS"""


""" 1. starting the loop """

index = 0
while time2 - time1 < time_run:       #can change time (seconds)
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
            if ((len(a) == 4)):
                #if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>4 & len(a[3])>4):
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                all_data.append([x1,y1,x2,y2])
                print(a)
                if distance_limit:
                    print(distance([x1,y1,x2,y2], all_data[-1])>epsilon)
                    if len(all_data) == 2:
                        ax1.scatter(x1,y1,s=10, color = "y")
                        ax2.scatter(x2,y2,s=10, color = "y")
                        plt.show()
                    elif distance([x1,y1,x2,y2], all_data[-1])>epsilon:
                        print("hi")
                        ax1.scatter(x1,y1,s=10, color = "y")
                        ax2.scatter(x2,y2,s=10, color = "y")
                        plt.show()
                else:
                    ax1.scatter(x1,y1,s=10, color = "y")
                    ax2.scatter(x2,y2,s=10, color = "y")
                    plt.show()
                plt.pause(0.000000001)
                        
                    
                        
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

alldata = np.transpose(np.asarray(all_data[1:]))

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, clusters, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)
#print(cluster_membership)

""" 4. plotting the points according to membership + plotting centroids """

for j in range(clusters):              #change depending on number clusters
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax1.plot(alldata[0][i], alldata[1][i], '.', color = colors[j])
            ax2.plot(alldata[2][i], alldata[3][i], '.', color = colors[j])
    ax1.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
    ax2.plot(cntr[j][2], cntr[j][3], colors[j]+"s")
    
""" 5. adding line between centroids """

"""for point in cntr:
    for point2 in cntr:
        plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")"""
        
""" 6. saving the figure as a png file """
plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\figa' + num + '.png')
#plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig1' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\figa' + num + '.png')
        
        
""" 7. resetting the plot with only centroids """

fig2, (ax3, ax4) = plt.subplots(1, 2, sharey=True, figsize = (16,8))
ax3.axis([left,right,left,right])
ax4.axis([left,right,left,right])
for j in range(5):              #change value to match clusters
    ax3.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
    ax4.plot(cntr[j][2], cntr[j][3], colors[j]+"s")

""" C. SECOND LOOP (RUNS INDEFINITELY) """


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
            if ((len(a) == 4)):
                #if (len(a[0])>=4 & len(a[1])>=4 & len(a[2])>4 & len(a[3])>4):
                #time100 = time.time()
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                a_array = np.asarray([[x1], [y1], [x2], [y2]])
                v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                cluster_num = np.argmax(v[0], axis = 0)
                cluster_num = int(cluster_num)
                ax3.scatter(x1,y1,s=50, color = colors[cluster_num])
                ax4.scatter(x2,y2,s=50, color = colors[cluster_num])
                # if distance_limit:
                #     if distance([x1,y1,x2,y2], all_data[-1])>epsilon:
                #         ax3.scatter(x1,y1,s=50, color = colors[cluster_num])
                #         ax4.scatter(x2,y2,s=50, color = colors[cluster_num])
                # else:
                #     ax3.scatter(x1,y1,s=50, color = colors[cluster_num])
                #     ax4.scatter(x2,y2,s=50, color = colors[cluster_num])
                plt.pause(0.000000001)
                plt.pause(0.000000001)
                ax3.clear()
                ax4.clear()
                ax3.axis([left,right,left,right])
                ax4.axis([left,right,left,right])
                #plt.remove()
                #plt.axis([0,100,0,100])
                for j in range(clusters):              #change value to match clusters
                    ax3.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
                    ax4.plot(cntr[j][2], cntr[j][3], colors[j]+"s")
                        
                        #time101 = time.time()
                        #print ("FPS:" + str(1/(time101-time100)))
                        
        #index += 1
            line = []


ser.close()
