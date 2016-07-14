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
record_time = 120

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

print("connected to: " + ser.portstr)
line = []           #storing the numbers until it reaches a space
index = 0           #for some reason the first value is buggy, use this so circumvent
all_data = [["logrms1","logrms2"]]
all_data_conv = [["logrms1conv", "logrms2conv"]]
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']

""" 4. initializing plot and time """

fig0 = plt.figure(0)
ax = plt.axes(projection = "3d")
#ax.set_xlim(2,4)
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_zlim(0,20)
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
                
                converted = threeDconv([[x],[y],[z]])
                all_data_conv.append([converted[0][0], converted[1][0], converted[2][0]])
                ax.scatter(converted[0][0],converted[1][0],converted[2][0], c='y', s=10, marker = "o")
                #ax.scatter(x,y,z, c='y', s=10, marker = "o")
                
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
#alldata = np.transpose(np.asarray(all_data_conv[1:]))

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 5, 2, error=0.0005, maxiter=10000, init=None, seed=None) #second par is clusters
cluster_membership = np.argmax(u, axis=0)
#print(cluster_membership)

""" 4. plotting the points according to membership + plotting centroids """

alldata = np.transpose(np.asarray(all_data_conv[1:])) ##option 2
cntr2 = np.transpose(np.array(threeDconv(np.transpose(cntr)))) ##option2
print (cntr)
print (cntr2)
#cntr2 = cntr

for j in range(5):              #change depending on number clusters
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i], marker = 'o', c = colors[j], s = 50)
    ax.scatter(cntr2[j][0], cntr2[j][1], cntr2[j][2], c = colors[j], marker = "s", s = 50)
    
    
""" 5. adding line between centroids """

"""for point in cntr2:
    for point2 in cntr2:
        ax.plot([point[0], point2[0]], [point[1], point2[1], [point[2],[point2[2]],"-b")"""
        
""" 6. saving the figure as a png file """

plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')
        
        
""" 7. resetting the plot with only centroids """

fig1 = plt.figure(1)
ax = plt.axes(projection = "3d")
for j in range(5):              #change value to match clusters
    ax.scatter(cntr2[j][0], cntr2[j][1], cntr2[j][2], c = colors[j], marker = "s", s = 50)

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
                
                #ax.scatter(x,y,z, c='y', s=10, marker = "o")
                
                converted = threeDconv([[x],[y],[z]])
                ax.scatter(converted[0][0],converted[1][0],converted[2][0], c=colors[j], s=50, marker = "o")
                
                plt.pause(0.000000001)
                plt.clf()
                fig1 = plt.figure(1)
                ax = plt.axes(projection = "3d")
                for j in range(5):              #change value to match clusters
                    ax.scatter(cntr2[j][0], cntr2[j][1], cntr2[j][2], c = colors[j], marker = "s", s = 50)
                    
            line = []



ser.close()