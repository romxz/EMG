<<<<<<< HEAD

"""This code collects data that has been pre-classified for each motion. 
For each motion, linear regression is performed up to the third root of the independent variable
The linear regression plot is graphed and the theta values are recorded. 
Upon reading a new sample of data (set to a certain array of points), linear regression is performed and the values are then classified according to the determined set

Table of Contents

A. SETUP
=======
"""
PLOTTING LIVE DATA AND ANALYSIS

FOR USE WITH ARDUINO CODE "NEW3D" (OR SIMILAR)

|||||Contents List|||||

A. Initialization and Setup
>>>>>>> origin
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
<<<<<<< HEAD
    2. Rest Centroid
    3. Save as CSV
    4. Save as PNG
    5. Logistic Regression
    6. Plot Reset
=======
    2. Centroids
    3. Covariance Matrix
    4. Save as CSV
    5. Save as PNG
    6. Multiclass Logistic Regression
    7. Plot Reset
>>>>>>> origin
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
motion_time = 20
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
for i in range(motion_num):
    motion_arrays.append([])
if sensor_num == 2:
    alldata = [["logrms1","logrms2","class"]]
    avg = [0, 0]
elif sensor_num == 3:
    alldata = [["logrms1","logrms2","logrms3","class"]]
    avg = [0,0,0]
elif sensor_num == 4:
    alldata = [["logrms1","logrms2","logrms3","logrms4","class"]]
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
cov_matrix = False
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

"""regular mode """

while current_motion_num < motion_num:
    time1 = time.time()
    time2 = time.time()
    index = 0
    while time2 - time1 < motion_time:
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
                x0 = float(a[0])
                x1 = float(a[1])
                x2 = float(a[2])
                x3 = float(a[3])
                x0x0 = float(a[0])*float(a[0])
                x0x0x0 = float(a[0])*float(a[0])*float(a[0])
                x2x2 = float(a[2])*float(a[2])
                x2x2x2 = float(a[2])*float(a[2])*float(a[2])
                alldata.append([x0,x1,x2,x3])
                for i in range(motion_num):
                    if current_motion_num == i:
                        motion_arrays[i].append([x0,x0x0,x0x0x0,x1,x2,x2x2,x2x2x2,x3])
                ax1.scatter(x0,x1,s=30,c = colors[current_motion_num])
                ax2.scatter(x2,x3,s=30,c = colors[current_motion_num])
                plt.show()
                plt.pause(0.00001)
                
                avg = np.divide([sum(x) for x in zip(np.multiply((n-1),[avg])[0].tolist(), [x0,x1,x2,x3])],n).tolist()
                n += 1
                
                
        line = []
        index += 1
        time2 = time.time()
        
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
    
    t2 = np.arange(-10, 10, 0.1)
    
    i = motion_arrays[current_motion_num]
    if not (i==0):
        for j in range(0, len(i)):
            y1a.append(i[j][3])
            x1a.append(i[j][0:3])
            y2a.append(i[j][7])
            x2a.append(i[j][4:7])
        x1a = np.ndarray.tolist(np.transpose(np.array(x1a)))
        x2a = np.ndarray.tolist(np.transpose(np.array(x2a)))
        x1a = np.column_stack(x1a+[[1]*len(x1a[0])])
        beta_hat1 = np.ndarray.tolist(np.linalg.lstsq(x1a,y1a)[0])
        x2a = np.column_stack(x2a+[[1]*len(x2a[0])])
        beta_hat2 = np.ndarray.tolist(np.linalg.lstsq(x2a,y2a)[0])
        alldata.append(beta_hat1+beta_hat2+[current_motion_num])
        
        ax1.plot(t2, beta_hat1[0]*t2 + beta_hat1[1]*t2*t2 + beta_hat1[2]*t2*t2*t2 + beta_hat1[3],colors[current_motion_num])
        ax2.plot(t2, beta_hat2[0]*t2 + beta_hat2[1]*t2*t2 + beta_hat2[2]*t2*t2*t2 + beta_hat2[3],colors[current_motion_num])
        plt.show()
    
        x1a = []
        y1a = []
        x2a = []
        y2a = []    
    
    if prompt == True:
        input("next")
    index = 0
    print("next mot")
            
    current_motion_num += 1
    ser.reset_input_buffer()
    ser.reset_output_buffer()

""" 2. Rest Centroid """

print("Recording has completed.")

rest_centroid = [centres[0][0], centres[0][1], centres[0][2], centres[0][3]]
fig0
ax1.scatter(centres[0][0], centres[0][1], c = colors[i], s = 50, marker = "s")
ax2.scatter(centres[0][2], centres[0][3], c = colors[i], s = 50, marker = "s")


""" 3. Save as CSV """

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
        for i in alldata:
            writer.writerow(i)
    print ("Saved as CSV")
                
""" 4. Save as PNG """

if store_image == True:
    plt.savefig(newpath + "\\fig"  + num + '.png')
    print ("Saved as PNG")
    

""" 5. Logistic Regression """


for i in range(len(alldata)):
    x_mat.append(alldata[i][0:-1])
    y_vec.append([alldata[i][-1]])
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
    for i in range(len(alldata)):
    
        y_vec.append([alldata[i][-1]])


""" 6. Plot Reset """

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


""" C. CONTINUOUS DATA TRACKING """
y1_values = []
x1_values = []
y2_values = []
x2_values = []

list_size = 0
curr_index = 0
curr_list_pos = 0
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
                x0 = float(a[0])
                x1 = float(a[1])
                x2 = float(a[2])
                x3 = float(a[3])
                x0x0 = float(a[0])*float(a[0])
                x0x0x0 = float(a[0])*float(a[0])*float(a[0])
                x2x2 = float(a[2])*float(a[2])
                x2x2x2 = float(a[2])*float(a[2])*float(a[2])
                
                if list_size<10:
                    y1_values.append(x1)
                    x1_values.append([x0,x0x0,x0x0x0])
                    y2_values.append(x3)
                    x2_values.append([x2,x2x2,x2x2x2])
                    list_size += 1
                    for i in range(len(list_size)): # print the shit
                        ax3.scatter(x1_values[i],y1_values[i],s=50, color = "k")
                        ax4.scatter(x2_values[i],y2_values[i],s=50, color = "k")
                
                elif list_size == 10:
                    
                    y1_values[curr_index] = (x1)
                    x1_values[curr_index] = ([x0,x0x0,x0x0x0])
                    y2_values[curr_index] = (x3)
                    x2_values[curr_index] = ([x2,x2x2,x2x2x2])
                    
                    x1 = np.ndarray.tolist(np.transpose(np.array(x1)))
                    x2 = np.ndarray.tolist(np.transpose(np.array(x2)))
                    x1 = np.column_stack(x1+[[1]*len(x1[0])])
                    beta_hat1 = np.ndarray.tolist(np.linalg.lstsq(x1,y1)[0])
                    x2 = np.column_stack(x2+[[1]*len(x2[0])])
                    beta_hat2 = np.ndarray.tolist(np.linalg.lstsq(x2,y2)[0])
                    curr_index += 1
                    
                    for i in range(motion_num):
                        probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[beta_hat1[0]],[beta_hat1[1]],[beta_hat1[2]],[beta_hat1[3]],[beta_hat2[0]],[beta_hat2[1]],[beta_hat2[2]],[beta_hat2[3]]]))))
                    if distance([x0,x1,x2,x3],[centres[0][0], centres[0][1], centres[0][2], centres[0][3]]) > 2.0: 
                        cluster_num = np.argmax(probabilities)
                    else:
                        cluster_num = 0
                    
                    for i in range(len(10)):
                        ax3.scatter(x1_values[i],y1_values[i],s=50, color = colors[cluster_num])
                        ax4.scatter(x2_values[i],y2_values[i],s=50, color = colors[cluster_num])
                    plt.pause(0.0000001)
                    ax3.clear()
                    ax4.clear()
                    ax3.axis([xmin,xmax,ymin,ymax])
                    ax4.axis([xmin2,xmax2,ymin2,ymax2])
                
                if curr_index == 10:
                    curr_index = 1
                    
                
                
        
                        
        line = []
        probabilities = []


ser.close()
