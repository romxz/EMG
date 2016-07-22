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
time_run = 20
clusters = 4
xmax = 7
xmin = -2
ymax = 7
ymin = -2
#for 3D
zmax = 7
zmin = -2
#for 4D
xmax2 = 7
xmin2 = -2
ymax2 = 7
ymin2 = -2

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
cent_lines = True
second_loop = True
converted = False  #for 3D
    
""" 6. Serial """

ser = serial.Serial(port='COM6',baudrate=9600,timeout=None)
print("connected to: " + ser.portstr)

""" 7. Plot """

if sensor_num == 2:
    fig0 = plt.figure(0)
    plt.axis([xmin,xmax,ymin,ymax])
elif sensor_num == 3:
    fig0 = plt.figure(0)
    ax = plt.axes(projection = "3d")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.set_zlim(zmin,zmax)
elif sensor_num == 4:
    fig0, (ax1, ax2) = plt.subplots(1, 2, figsize = (16,8))
    ax1.axis([xmin,xmax,ymin,ymax])
    ax2.axis([xmin2,xmax2,ymin2,ymax2])
plt.ion()

""" 8. Time """
time1 = time.time()
time2 = time.time()



""" B. DATA COLLECTION AND ANALYSIS """

""" 1. Loop """

while cont_mode:
    if index>=20:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
    c = ser.readline()
    c = (str(c)[2:-5])
    c = c.split(",")
    
    try:
        a = [float(i) for i in c]
    except ValueError:
        try:
            a = a
        except NameError:
            if sensor_num == 2:
                a = [0.1,0.1]
            elif sensor_num == 3:
                a = [0.1,0.1,0.1]
            elif sensor_num == 4:
                a = [0.1,0.1,0.1,0.1]
        
    if sensor_num == 4:
        if ((len(a) == 4)):
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<xmax2 \
                and a[2]>xmin2 and a[3]<ymax2 and a[3]>ymin2):
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                ax1.scatter(x1,y1,s=10, color = "y")
                ax2.scatter(x2,y2,s=10, color = "y")
                plt.show()
                plt.pause(0.000000001)
                ax1.clear()
                ax2.clear()
                ax1.axis([xmin,xmax,ymin,ymax])
                ax2.axis([xmin2,xmax2,ymin2,ymax2])
                    
    elif sensor_num == 3:
        if ((len(a) == 3)):
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<zmax \
                and a[2]>zmin):
                x = float(a[0])
                y = float(a[1])
                z = float(a[2])
                    
                if converted:  
                    converted_xyz = threeDconv([[x],[y],[z]])
                    x = converted_xyz[0][0]
                    y = converted_xyz[1][0]
                    z = converted_xyz[2][0]
        
                ax.scatter(x,y,z, c='y', s=10, marker = "o")
                plt.pause(0.00000001)
                ax.clear()
                ax = plt.axes(projection = "3d")
                ax.set_xlim(xmin,xmax)
                ax.set_ylim(ymin,ymax)
                ax.set_zlim(zmin,zmax)
        
    elif sensor_num == 2: 
        if ((len(a) == 2)): 
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin):        
                x = float(a[0])
                y = float(a[1])
                plt.scatter(x,y,s=10, color = "y")
                plt.pause(0.000000001)
                plt.clf()
                plt.axis([xmin,xmax,ymin,ymax])
                        
            
    line = []
         
    index += 1




while time2 - time1 < time_run:    

    if index>=20:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
    c = ser.readline()
    c = (str(c)[2:-5])
    c = c.split(",")
    
    try:
        a = [float(i) for i in c]
    except ValueError:
        try:
            a = a
        except NameError:
            if sensor_num == 2:
                a = [0.1,0.1]
            elif sensor_num == 3:
                a = [0.1,0.1,0.1]
            elif sensor_num == 4:
                a = [0.1,0.1,0.1,0.1]
            
    if sensor_num == 4:
        if ((len(a) == 4)):
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<xmax2 \
                and a[2]>xmin2 and a[3]<ymax2 and a[3]>ymin2):
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                all_data.append([x1,y1,x2,y2])
                ax1.scatter(x1,y1,s=10, color = "y")
                ax2.scatter(x2,y2,s=10, color = "y")
                plt.show()
                plt.pause(0.000001)
                # ax1.clear()
                # ax2.clear()
                # ax1.axis([xmin,xmax,ymin,ymax])
                # ax2.axis([xmin2,xmax2,ymin2,ymax2])
                    
    elif sensor_num == 3:
        if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<zmax \
            and a[2]>zmin):
            if ((len(a) == 3)):
                x = float(a[0])
                y = float(a[1])
                z = float(a[2])
                    
                if converted:  
                    converted_xyz = threeDconv([[x],[y],[z]])
                    x = converted_xyz[0][0]
                    y = converted_xyz[1][0]
                    z = converted_xyz[2][0]
                
                all_data.append([x,y,z])
                ax.scatter(x,y,z, c='y', s=10, marker = "o")
                plt.pause(0.00000001)
                # ax.clear()
                # ax = plt.axes(projection = "3d")
                # ax.set_xlim(xmin,xmax)
                # ax.set_ylim(ymin,ymax)
                # ax.set_zlim(zmin,zmax)
        
    elif sensor_num == 2:   
        if ((len(a) == 2)):   
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin):  
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y])
                plt.scatter(x,y,s=10, color = "y")
                plt.pause(0.000000001)
                # plt.clf()
                # plt.axis([xmin,xmax,ymin,ymax])
                #             
            
    line = []
    time2 = time.time()
    index += 1

    
""" 2. Save as CSV """

num1 = datetime.datetime.now().date() 
num2 = datetime.datetime.now().time() 
num =  num1.isoformat() + "..." + num2.isoformat()
num3 = str(datetime.datetime.now().date().isoformat()).replace("-",".")
num = (str(num).replace(":","-"))
num = (str(num).replace("-","."))

newpath = ('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\'+num3) 
if not os.path.exists(newpath):
    os.makedirs(newpath)

if store_data == True:
    #change save location below
    with open("newpath" + '\\test' + num + '.csv', 'w', newline='') as csvfile:
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

if sensor_num == 2:
    fig2 = plt.figure(2)
    plt.axis([xmin,xmax,ymin,ymax])
elif sensor_num == 3:
    fig2 = plt.figure(2)
    ax = plt.axes(projection = "3d")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.set_zlim(zmin,zmax)
elif sensor_num == 4:
    fig2, (ax5, ax6) = plt.subplots(1, 2, figsize = (16,8))
    ax5.axis([xmin,xmax,ymin,ymax])
    ax6.axis([xmin2,xmax2,ymin2,ymax2])
plt.ion()

for j in range(clusters):
    
    if sensor_num == 2:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                plt.plot(alldata[0][i], alldata[1][i], '.', color = colors[j])
        plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
        
    if sensor_num == 3:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax.scatter(alldata[0][i], alldata[1][i], alldata[2][i], marker = 'o', c = colors[j], s = 50)
        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
    
    if sensor_num == 4:
        for i in range(len(cluster_membership)):
            if cluster_membership[i] == j:
                ax5.plot(alldata[0][i], alldata[1][i], '.', color = colors[j])
                ax6.plot(alldata[2][i], alldata[3][i], '.', color = colors[j])
        ax5.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
        ax6.plot(cntr[j][2], cntr[j][3], colors[j]+"s")

""" 5. Centroid Lines """

if cent_lines == True:
    for point in cntr:
        for point2 in cntr:
            
            if sensor_num == 2:
                plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")
        
            elif sensor_num == 3:
                ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
                
            elif sensor_num == 4:
                ax5.plot([point[0], point2[0]], [point[1], point2[1]],"-b")
                ax6.plot([point[2], point2[2]], [point[3], point2[3]],"-b")
                
""" 6. Save as PNG """

if store_image == True:
    plt.savefig("newpath" + "\\fig"  + num + '.png')
    print ("Saved as PNG")

""" 7. Plot Reset """

if sensor_num == 2:
    fig1 = plt.figure(1)
    plt.axis([xmin,xmax,ymin,ymax])
elif sensor_num == 3:
    fig1 = plt.figure(1)
    ax = plt.axes(projection = "3d")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.set_zlim(zmin,zmax)
elif sensor_num == 4:
    fig1, (ax3, ax4) = plt.subplots(1, 2, figsize = (16,8))
    ax3.axis([xmin,xmax,ymin,ymax])
    ax4.axis([xmin2,xmax2,ymin2,ymax2])
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
        if index>=20:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
        c = ser.readline()
        c = (str(c)[2:-5])
        c = c.split(",")
        
        try:
            a = [float(i) for i in c]
        except ValueError:
            try:
                a = a
            except NameError:
                if sensor_num == 2:
                    a = [0.1,0.1]
                elif sensor_num == 3:
                    a = [0.1,0.1,0.1]
                elif sensor_num == 4:
                    a = [0.1,0.1,0.1,0.1]
                    
        if sensor_num == 4:
            if ((len(a) == 4)):
                if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<xmax2 \
                    and a[2]>xmin2 and a[3]<ymax2 and a[3]>ymin2):
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
                    plt.pause(0.000000001)
                    plt.pause(0.000000001)
                    ax3.clear()
                    ax4.clear()
                    ax3.axis([xmin,xmax,ymin,ymax])
                    ax4.axis([xmin2,xmax2,ymin2,ymax2])
                    for j in range(clusters):              
                        ax3.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
                        ax4.plot(cntr[j][2], cntr[j][3], colors[j]+"s")
        
        elif sensor_num == 3:
            if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin and a[2]<zmax \
                and a[2]>zmin):
                if ((len(a) == 3)):
                    x = float(a[0])
                    y = float(a[1])
                    z = float(a[2])
                    
                    if converted:
                        converted_xyz = threeDconv([[x],[y],[z]])
                        x = converted_xyz[0][0]
                        y = converted_xyz[1][0]
                        z = converted_xyz[2][0]
                        
                    a_array = np.asarray([[x], [y], [z]])
                    v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                    cluster_num = np.argmax(v[0], axis = 0)
                    cluster_num = int(cluster_num)
                    ax.set_xlim(xmin,xmax)
                    ax.set_ylim(ymin,ymax)
                    ax.set_zlim(zmin,zmax)
                    ax.scatter(x,y,z,s=40, c = colors[cluster_num])
                    plt.pause(0.000000001)
                    ax.clear()
                    ax.set_xlim(xmin,xmax)
                    ax.set_ylim(ymin,ymax)
                    ax.set_zlim(zmin,zmax)
                    fig1 = plt.figure(1)
                    ax = plt.axes(projection = "3d")
                    for j in range(clusters):            
                        ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)
        
        elif sensor_num == 2:
            if ((len(a) == 2)):
                if (a[0]<xmax and a[0]>xmin and a[1]<ymax and a[1]>ymin):
                    x = float(a[0])
                    y = float(a[1])
    
                    a_array = np.asarray([[x], [y]])
                    v = fuzz.cluster.cmeans_predict(a_array, cntr, 2, error = 0.0005, maxiter = 10000)
                    cluster_num = np.argmax(v[0], axis = 0)
                    cluster_num = int(cluster_num)
                    plt.scatter(x,y,s=40, c = colors[cluster_num])
                    plt.pause(0.000000001)
                    plt.clf()
                    plt.axis([xmin,xmax,ymin,ymax])
                    for j in range(clusters):   
                        plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
    
                        
                        
        line = []


ser.close()
