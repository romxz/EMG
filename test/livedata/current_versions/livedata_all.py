"""
PLOTTING LIVE DATA AND ANALYSIS

FOR USE WITH ARDUINO CODE "NEW3D" (OR SIMILAR)

|||||Contents List|||||

A. Initialization and Setup
    1. Libraries
    2. Constants
    3. Variables
    4. Functions
    5. Options
    6. Serial
    7. Plot
    8. Time
B. Data Collection and Analysis 
    1. Loop
    2. Save as CSV
    3. Fuzzy C Means
    4. Clusters
    5. Centroid Lines
    6. Save as PNG
    7. Plot Reset
C. Continuous Data Tracking
    
"""



""" A. INITIALIZATION AND SETUP """

""" 1. Libraries """

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

""" 2. Constants """

sensor_num = 2
record_time = 120
clusters = 4
scale_left = -1 
scale_right = 9
converted =   #for 3D
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'w']

""" 3. Variables """

line = []
index = 0
if sensor_num == 2:
    all_data = [["logrms1","logrms2"]]
elif sensor_num == 3:
    all_data = [["logrms1","logrms2","logrms3"]]
elif sensor_num == 4:
    all_data = [["logrms1","logrms2","logrms3","logrms4"]]

""" 4. Functions """

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

""" 5. Options """

cont_mode = False
store_data = False
store_image = False
cent_lines = False
second_loop = False
    
""" 6. Serial """

ser = serial.Serial(port='COM10',baudrate=9600,timeout=None)
print("connected to: " + ser.portstr)

""" 7. Plot """

if sensor_num == 2:
    fig0 = plt.figure(0)
    plt.axis([scale_left,scale_right,scale_left,scale_right])
elif sensor_num == 3:
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")
    ax.set_xlim(scale_left,scale_right)
    ax.set_ylim(scale_left,scale_right)
    ax.set_zlim(scale_left,scale_right)
elif sensor_num == 4:
    fig0, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,8))
    ax1.axis([left1,right1,left2,right2])
    ax2.axis([left3,right3,left4,right4])
plt.ion()

""" 8. Time """
time1 = time.time()
time2 = time.time()



""" B. DATA COLLECTION AND ANALYSIS """

""" 1. Loop """

while time2 - time1 < time_run:    

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
            if sensor_num == 4:
                if ((len(a) == 4)):
                    x1 = float(a[0])
                    y1 = float(a[1])
                    x2 = float(a[2])
                    y2 = float(a[3])
                    all_data.append([x1,y1,x2,y2])
                    print(a)
                    if (x1>left1 and x1<right1 and x2>left2 and x2<right2 and y1>left3 and y1<right3 and y2>left4 and y2<right4):
                            ax1.scatter(x1,y1,s=10, color = "y")
                            ax2.scatter(x2,y2,s=10, color = "y")
                            plt.show()
                    plt.pause(0.000000001)
                    
            if sensor_num == 3:
                if (len(a) == 3):
                    x = float(a[0])
                    y = float(a[1])
                    z = float(a[2])
                    
                    if converted:  
                        converted_xyz = threeDconv([[x],[y],[z]])
                        x = converted_xyz[0][0]
                        y = converted_xyz[1][0]
                        z = converted_xyz[2][0]
                    if (x<scale_right and y<scale_right and z<scale_right and x>scale_left and y>scale_left and z>scale_left):
                        all_data.append([x,y,z])
                        ax.scatter(x,y,z, c='y', s=10, marker = "o")
                        plt.pause(0.00000001)
                        time2 = time.time()
                                            
            if sensor_num == 2:               
                if ((len(a) == 2)):
                    if (len(a[0])>=4 & len(a[1])>=4):
                        #time100 = time.time()
                        x = float(a[0])
                        y = float(a[1])
                        all_data.append([x,y])
                        plt.scatter(x,y,s=10, color = "y")
                        plt.pause(0.000000001)
            
            line = []
         
    index += 1
    time2 = time.time()
    
""" 2. Save as CSV """

if store_data == True:
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
    print ("Saved as CSV")
            
""" 3. Fuzzy C Means """

alldata = np.transpose(np.asarray(all_data[1:]))
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, clusters, 2, error=0.0005, maxiter=10000, init=None, seed=None) 
cluster_membership = np.argmax(u, axis=0)

""" 4. Clusters """

for j in range(clusters):
    
    if sensor_num == 2:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                plt.plot(x_val[i], y_val[i], '.', color = colors[j])
        plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
        
    if sensor_num == 3:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i], marker = 'o', c = colors[j], s = 50)
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    
    if sensor_num == 4:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax1.plot(alldata[0][i], alldata[1][i], '.', color = colors[j])
                ax2.plot(alldata[2][i], alldata[3][i], '.', color = colors[j])
        ax1.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
        ax2.plot(cntr[j][2], cntr[j][3], colors[j]+"s")

""" 5. Centroid Lines """

if cent_lines == True:
    for point in cntr:
        for point2 in cntr:
            
            if sensor_num == 2:
                plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")
        
            elif sensor_num == 3:
                ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
                
            elif sensor_num == 4:
                ax1.plot([point[0], point2[0]], [point[1], point2[1]],"-b")
                ax2.plot([point[2], point2[2]], [point[3], point2[3]],"-b")
                
""" 6. Save as PNG """

if store_image == True:
    plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\fig' + num + '.png')
    print ("figure saved as: "+ 'C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\csvfiles\\fig' + num + '.png')

""" 7. Plot Reset """

if sensor_num == 2:
    fig1 = plt.figure(1)
    plt.axis([scale_left,scale_right,scale_left,scale_right])
elif sensor_num == 3:
    fig1 = plt.figure(1)
    ax = plt.axes(projection = "3d")
    ax.set_xlim(scale_left,scale_right)
    ax.set_ylim(scale_left,scale_right)
    ax.set_zlim(scale_left,scale_right)
elif sensor_num == 4:
    fig1, (ax3, ax4) = plt.subplots(1, 2, figsize = (16,8))
    ax3.axis([left1,right1,left2,right2])
    ax4.axis([left3,right3,left4,right4])
plt.ion()

for j in range(clusters):
    if sensor_num == 2:
        plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
    elif sensor_num == 3:
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    elif sensor_num == 4:
        ax3.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
        ax4.plot(cntr[j][2], cntr[j][3], colors[j]+"s")

""" C. CONTINUOUS DATA TRACKING """

if second_loop == True:
    while True:      
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
                
                if sensor_num == 4:
                    if ((len(a) == 4)):
                        x1 = float(a[0])
                        y1 = float(a[1])
                        x2 = float(a[2])
                        y2 = float(a[3])
                        if (x1>left1 and x1<right1 and x2>left2 and x2<right2 and y1>left3 and y1<right3 and y2>left4 and y2<right4):
                            a_array = np.asarray([[x1], [y1], [x2], [y2]])
                            v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                            cluster_num = np.argmax(v[0], axis = 0)
                            cluster_num = int(cluster_num)
                            ax3.scatter(x1,y1,s=50, color = colors[cluster_num])
                            ax4.scatter(x2,y2,s=50, color = colors[cluster_num])
                            plt.pause(0.000000001)
                            plt.pause(0.000000001)
                            ax3.clear()
                            ax4.clear()
                            ax3.axis([left1,right1,left2,right2])
                            ax4.axis([left3,right3,left4,right4])
                            for j in range(clusters):              
                                ax3.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
                                ax4.plot(cntr[j][2], cntr[j][3], colors[j]+"s")
                
                elif sensor_num == 3:
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
                
                elif sensor_num == 2:
                    if ((len(a) == 2)):
                        x = float(a[0])
                        y = float(a[1])
    
                        a_array = np.asarray([[x], [y]])
                        v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                        cluster_num = np.argmax(v[0], axis = 0)
                        cluster_num = int(cluster_num)
                        plt.scatter(x,y,s=40, c = colors[cluster_num])
                        plt.pause(0.000000001)
                        plt.clf()
                        for j in range(clusters):   
                            plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")

                            
                                
                line = []


ser.close()
