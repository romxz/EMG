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
    2. Centroids
    3. Covariance Matrix
    4. Save as CSV
    5. Save as PNG
    6. Multiclass Logistic Regression
    7. Plot Reset
C. Continuous Data Tracking
    
"""



""" A. INITIALIZATION AND SETUP """

""" 1. Libraries """

import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import math
import csv
import random
import datetime
import numpy as np
import scipy.optimize as op
import os
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")

""" 2. Constants """

sensor_num = 4
motion_time = 2
motion_num = 5
xmax = 8
xmin = 2
ymax = 8
ymin = 2
#for 3D
zmax = 8
zmin = 2
#for 4D
xmax2 = 8
xmin2 = 2
ymax2 = 8
ymin2 = 2
n = 1 # for avg
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'w']
delimiter = " "


""" 3. Variables """

centres = []
line = []
optimal_theta = []
probabilities = []
current_motion_num = 0
index = 0
if sensor_num == 2:
    all_data = [["logrms1","logrms2","class"]]
    avg = [0, 0]
elif sensor_num == 3:
    all_data = [["logrms1","logrms2","logrms3","class"]]
    avg = [0,0,0]
elif sensor_num == 4:
    all_data = [["logrms1","logrms2","logrms3","logrms4","class"]]
    avg = [0,0,0,0]

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

def sigmoid(matrix):
    return 1/(1 + np.exp(-matrix))

def gradient(theta,x,y):
    m , n = x.shape
    theta = theta.reshape((n,1))
    y = y.reshape((m,1))
    sigmoid_x_theta = sigmoid(x.dot(theta))
    grad = ((x.T).dot(sigmoid_x_theta-y))/m
    return grad.flatten()
    
def costfunc(theta,x,y):
    m,n = x.shape
    theta = theta.reshape((n,1))
    y = y.reshape((m,1))
    term1 = np.log(sigmoid(x.dot(theta))+0.00001)
    term2 = np.log(1-sigmoid(x.dot(theta))+0.00001)
    term1 = term1.reshape((m,1))
    term2 = term2.reshape((m,1))
    term = y * term1 + (1 - y) * term2
    J = -((np.sum(term))/m)
    return J
    
def distance(x,y):
    dist = 0
    for i in range(len(x)):
        dist += (x[i] - y[i])**2
    return math.sqrt(dist)
    
""" 5. Options """

cont_mode = False
store_data = True
store_image = True
second_loop = True
converted = False  #for 3D
centroids = True
cov_matrix = True
prompt = False
  
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

""" cont mode """

while cont_mode:
    if index>=20:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
    c = ser.readline()
    c = (str(c)[2:-5])
    c = c.split(delimiter)
    
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
            x = float(a[0])
            y = float(a[1])
            plt.scatter(x,y,s=10, color = "y")
            plt.pause(0.000000001)
            plt.clf()
            plt.axis([xmin,xmax,ymin,ymax])
                        

            
    line = []
         
    index += 1

"""regular mode """

while current_motion_num < motion_num:
    time1 = time.time()
    time2 = time.time()
    index = 0
    while time2 - time1 < motion_time:
        #if index>=20:
            #ser.reset_input_buffer()
            #ser.reset_output_buffer()
        c = ser.readline()
        c = (str(c)[2:-5])
        c = c.split(delimiter)
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
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                all_data.append([x1,y1,x2,y2,current_motion_num])
                ax1.scatter(x1,y1,s=30,c = colors[current_motion_num])
                ax2.scatter(x2,y2,s=30,c = colors[current_motion_num])
                plt.show()
                plt.pause(0.00001)
                
                if centroids == True:
                    avg = np.divide([sum(x) for x in zip(np.multiply((n-1),[avg])[0].tolist(), [x1,y1,x2,y2])],n).tolist()
                n += 1
                
                        
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
                
                all_data.append([x,y,z,current_motion_num])
                ax.scatter(x,y,z, c = colors[current_motion_num], s=10, marker = "o")
                plt.pause(0.00001)
                
            
                if centroids == True:
                    avg = np.divide([sum(x) for x in zip(np.multiply((n-1),[avg])[0].tolist(), [x,y,z])],n).tolist()
                n += 1
            
        elif sensor_num == 2:   
            if ((len(a) == 2)):            
                x = float(a[0])
                y = float(a[1])
                all_data.append([x,y,current_motion_num])
                plt.scatter(x,y,s=30,c = colors[current_motion_num])
                plt.pause(0.00001)
                
                if centroids == True:
                    avg = np.divide([sum(x) for x in zip(np.multiply((n-1),[avg])[0].tolist(), [x,y])],n).tolist()
                n += 1
                
        line = []
        index += 1
        time2 = time.time()
    if centroids == True:
        centres.append(avg)
        if sensor_num == 2:
            avg = [0, 0]
        elif sensor_num == 3:
            avg = [0,0,0]
        elif sensor_num == 4:
            avg = [0,0,0,0]
        n = 1
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    if prompt == True:
        input("next")
    index = 0
    print("next mot")
            
    current_motion_num += 1
    ser.reset_input_buffer()
    ser.reset_output_buffer()

""" 2. Centroids """

if centroids == True:
    for i in range(len(centres)):
        print(i)
        if sensor_num == 4:
            fig0
            ax1.scatter(centres[i][0], centres[i][1], c = colors[i], s = 50, marker = "s")
            ax2.scatter(centres[i][2], centres[i][3], c = colors[i], s = 50, marker = "s")
        elif sensor_num == 3:
            ax.scatter(centres[i][0], centres[i][1], centres[i][2], c = colors[i], s = 50, marker = "s")
        elif sensor_num == 2:
            plt.scatter(centres[i][0], centres[i][1], c = colors[i], s = 50, marker = "s")
    
print("Recording has completed.")
    
""" 3. Covariance Matrix """

all_data = all_data[1:]
if cov_matrix == True:
    all_data_cov = np.cov(np.transpose(np.array(all_data)[:,:-1]))
    print(all_data_cov)

""" 4. Save as CSV """

num1 = datetime.datetime.now().date() 
num2 = datetime.datetime.now().time() 
num3 = str(datetime.datetime.now().date().isoformat()).replace("-",".")
num =  num1.isoformat() + "..." + num2.isoformat()
num = (str(num).replace(":","-"))
num = (str(num).replace("-","."))

newpath = ('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles\\'+num3) 
if not os.path.exists(newpath):
    os.makedirs(newpath)

if store_data == True:
    #change save location below
    with open(newpath + '\\test' + num + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in all_data:
            writer.writerow(i)
    print ("Saved as CSV")
                
""" 5. Save as PNG """

if store_image == True:
    plt.savefig(newpath + "\\fig"  + num + '.png')
    print ("Saved as PNG")
    
""" 6. Multiclass Logistic Regression """



y_vec = [] 
x_mat = []
for i in range(len(all_data)):
    x_mat.append(all_data[i][0:-1])
    y_vec.append([all_data[i][-1]])
for i in range(motion_num):
    for j in range(len(y_vec)):
        if y_vec[j][0] == i:
            y_vec[j] = [1]
        else:
            y_vec[j] = [0]
    
    y_vec = np.array(y_vec)
    x_mat = np.array(x_mat)
    m , n = x_mat.shape
    initial_theta = np.zeros(n)
    Result = op.minimize(fun = costfunc, 
                                    x0 = initial_theta, 
                                    args = (x_mat, y_vec),
                                    method = 'TNC',
                                    jac = gradient)
    optimal_theta.append(Result.x)
    y_vec = []
    for i in range(len(all_data)):
    
        y_vec.append([all_data[i][-1]])



mult=1
probabilities = []
for x1 in range(xmin*mult, xmax*mult+1, 1):
    for y1 in range(ymin*mult, ymax*mult+1, 1):
        for x2 in range(xmin2*mult, xmax2*mult+1, 1):
            for y2 in range(ymin2*mult, ymax2*mult+1, 1):
                for i in range(len(optimal_theta)):
                    probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x1/mult],[y1/mult],[x2/mult],[y2/mult]]))))
                
                cluster_num = np.argmax(probabilities)
                ax1.scatter(x1/mult,y1/mult,s=150, marker ="s",color = colors[cluster_num])
                ax2.scatter(x2/mult,y2/mult,s=150, marker = "s", color = colors[cluster_num])
                print(probabilities)
                probabilities = []
print("HI")

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

mult=1 

for i in range(motion_num):
    for x1 in range(xmin*mult, xmax*mult, 1):
        for y1 in range(ymin*mult, ymax*mult, 1):
            for x2 in range(xmin2*mult, xmin2*mult, 1):
                for y2 in range(ymin2*mult, ymax2*mult, 1):
                    probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x1/mult],[y1/mult],[x2/mult],[y2/mult]]))))
                    if distance([x1/mult,y1/mult,x2/mult,y2/mult],[centres[0][0], centres[0][1], centres[0][2], centres[0][3]]) > 2: 
                        cluster_num = np.argmax(probabilities)
                    else:
                        cluster_num = 0

                    ax3.scatter(x1/mult,y1/mult,s=50, color = colors[cluster_num])
                    ax4.scatter(x2/mult,y2/mult,s=50, color = colors[cluster_num])


""" C. CONTINUOUS DATA TRACKING """

if second_loop == True:
    while True:      
        if index>=20:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        c = ser.readline()
        c = (str(c)[2:-5])
        c = c.split(delimiter)
        
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
                x1 = float(a[0])
                y1 = float(a[1])
                x2 = float(a[2])
                y2 = float(a[3])
                
                for i in range(motion_num):
                    probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x1],[y1],[x2],[y2]]))))
                if distance([x1,y1,x2,y2],[centres[0][0], centres[0][1], centres[0][2], centres[0][3]]) > 2: 
                    cluster_num = np.argmax(probabilities)
                else:
                    cluster_num = 0
                
                ax3.scatter(x1,y1,s=50, color = colors[cluster_num])
                ax4.scatter(x2,y2,s=50, color = colors[cluster_num])
                plt.pause(0.0000001)
                ax3.clear()
                ax4.clear()
                ax3.axis([xmin,xmax,ymin,ymax])
                ax4.axis([xmin2,xmax2,ymin2,ymax2])
        
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
                    
                for i in range(motion_num):
                    probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x],[y],[z]]))))
                
                cluster_num = np.argmax(probabilities)
                
                ax.scatter(x,y,z,s=40, c = colors[cluster_num])
                plt.pause(0.00001)
                ax.clear()
                ax = plt.axes(projection = "3d")
                ax.set_xlim(xmin,xmax)
                ax.set_ylim(ymin,ymax)
                ax.set_zlim(zmin,zmax)
                
                
    
        elif sensor_num == 2:
            if ((len(a) == 2)):
                x = float(a[0])
                y = float(a[1])

                for i in range(motion_num):
                    probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x],[y]]))))
                
                cluster_num = np.argmax(probabilities)
               
                plt.scatter(x,y,s=40, c = colors[cluster_num])
                plt.pause(0.00001)
                plt.clf()
                plt.axis([xmin,xmax,ymin,ymax])


                    
                        
        line = []
        probabilities = []


ser.close()
