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
motion_time =2
motion_num = 5
xmax = 10
xmin = -10
ymax = 10
ymin = -10
#for 3D
zmax = 8
zmin = 2
#for 4D
xmax2 = 10
xmin2 = -10
ymax2 = 10
ymin2 = -10
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
motion_arrays = []
for i in range(motion_num):
    motion_arrays.append([])
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
cov_matrix = False
prompt = False
  
""" 6. Serial """

#ser = serial.Serial(port='COM6',baudrate=9600,timeout=None)
#print("connected to: " + ser.portstr)

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

alldata = []
x1a = []
y1a = []
x2a = []
y2a = []
index = 0

while current_motion_num < motion_num:
    # if current_motion_num == motion_num:
    #     current_motion_num += 1
    #     continue
    time1 = time.time()
    time2 = time.time()
    while time2 - time1 < motion_time:
        #if index>=20:
            #ser.reset_input_buffer()
            #ser.reset_output_buffer()
        a = random.random()
        x_val = a*20-10
        if current_motion_num == 0:
            c = [x_val,-2.5*x_val+random.random(),x_val,2*x_val+random.random()]
        elif current_motion_num == 1:
            c = [x_val,1*x_val+1+random.random(),x_val,-3*x_val+random.random()]
        elif current_motion_num == 2:
            c = [x_val,x_val**2+3+random.random(),x_val,0.15*x_val-3.4+random.random()]
        elif current_motion_num == 3:
            c = [x_val,x_val*-0.3+5+random.random(),x_val,x_val*0.5+3+random.random()]
        elif current_motion_num == 4:
            c = [x_val,1/3*x_val**3-5,x_val,-4+x_val**2]
        elif current_motion_num == 6:
            c = [-20,-20,-20,-20]
            
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
                if current_motion_num < motion_num:
                    x0 = float(a[0])
                    x1 = float(a[1])
                    x2 = float(a[2])
                    x3 = float(a[3])
                    x0x0 = float(a[0])*float(a[0])
                    x0x0x0 = float(a[0])*float(a[0])*float(a[0])
                    x2x2 = float(a[2])*float(a[2])
                    x2x2x2 = float(a[2])*float(a[2])*float(a[2])
                    all_data.append([x0,x1,x2,x3])
                    for i in range(motion_num):
                        if current_motion_num == i:
                            motion_arrays[i].append([x0,x0x0,x0x0x0,x1,x2,x2x2,x2x2x2,x3])
                    ax1.scatter(x0,x1,s=30,c = colors[current_motion_num])
                    ax2.scatter(x2,x3,s=30,c = colors[current_motion_num])
                    plt.show()
                    plt.pause(0.00001)
                    
                    if centroids == True:
                        avg = np.divide([sum(x) for x in zip(np.multiply((n-1),[avg])[0].tolist(), [x0,x1,x2,x3])],n).tolist()
                    n += 1
                
                
        line = []
        time2 = time.time()
        
    
    
    t2 = np.arange(-10, 10, 0.1)
    i = motion_arrays[current_motion_num]
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
    alldata.append(beta_hat1+beta_hat2+[index])
    print(beta_hat1)
    print(beta_hat2)
    print(index)
    ax1.plot(t2, beta_hat1[0]*t2 + beta_hat1[1]*t2*t2 + beta_hat1[2]*t2*t2*t2 + beta_hat1[3],colors[index])
    ax2.plot(t2, beta_hat2[0]*t2 + beta_hat2[1]*t2*t2 + beta_hat2[2]*t2*t2*t2 + beta_hat2[3],colors[index])
    plt.show()
    
    index += 1
    x1a = []
    y1a = []
    x2a = []
    y2a = []    
    print(current_motion_num)
            
    current_motion_num += 1
    # ax1.axis([xmin,xmax,ymin,ymax])
    # ax2.axis([xmin2,xmax2,ymin2,ymax2])
    # ax1.plot(t2, -2.5*t2, 'b')
    # ax1.plot(t2, t2+1, 'b')
    # ax1.plot(t2, t2**2+3, '-b')
    # ax1.plot(t2, t2*-0.3+5, '-b')
    # ax1.plot(t2, 1/3*t2**3-5, '-b')
    # ax2.plot(t2, t2*2, '-b')
    # ax2.plot(t2, t2*-3, '-b')
    # ax2.plot(t2, 0.15*t2-3, '-b')
    # ax2.plot(t2, t2*0.5+3, '-b')
    # ax2.plot(t2, t2**2-4, '-b')



""" 6. Linear Regression """
alldata = []
x1 = []
y1 = []
x2 = []
y2 = []
index = 0
t2 = np.arange(-10, 10, 0.1)
for i in motion_arrays:
    
    for j in range(1, len(i)):
        y1.append(i[j][3])
        x1.append(i[j][0:3])
        y2.append(i[j][7])
        x2.append(i[j][4:7])
    x1 = np.ndarray.tolist(np.transpose(np.array(x1)))
    x2 = np.ndarray.tolist(np.transpose(np.array(x2)))
    x1 = np.column_stack(x1+[[1]*len(x1[0])])
    beta_hat1 = np.ndarray.tolist(np.linalg.lstsq(x1,y1)[0])
    x2 = np.column_stack(x2+[[1]*len(x2[0])])
    beta_hat2 = np.ndarray.tolist(np.linalg.lstsq(x2,y2)[0])
    alldata.append(beta_hat1+beta_hat2+[index])
    # ax1.plot(t2, beta_hat1[0]*t2 + beta_hat1[1]*t2*t2 + beta_hat1[2]*t2*t2*t2 + beta_hat1[3],"b")
    index += 1
    x1 = []
    y1 = []
    x2 = []
    y2 = []
#print(alldata)





        # if current_motion_num == 0:
        #     c = [x_val,-2.5*x_val+random.random(),x_val,2*x_val+random.random()]
        # elif current_motion_num == 1:
        #     c = [x_val,1*x_val+1+random.random(),x_val,-3*x_val+random.random()]
        # elif current_motion_num == 2:
        #     c = [x_val,x_val**2+3+random.random(),x_val,0.15*x_val-3.4+random.random()]
        # elif current_motion_num == 3:
        #     c = [x_val,x_val*-0.3+5+random.random(),x_val,x_val*0.5+3+random.random()]
        # elif current_motion_num == 4:
        #     c = [x_val,1/3*x_val**3-5,x_val,-4+x_val**2]
        #     

y_vec = [] 
x_mat = []
all_data= alldata
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


""" 7. Plot Reset """

# if sensor_num == 2:
#     fig1 = plt.figure(1)
#     plt.axis([xmin,xmax,ymin,ymax])
# elif sensor_num == 3:
#     fig1 = plt.figure(1)
#     ax = plt.axes(projection = "3d")
#     ax.set_xlim(xmin,xmax)
#     ax.set_ylim(ymin,ymax)
#     ax.set_zlim(zmin,zmax)
# elif sensor_num == 4:
#     fig1, (ax3, ax4) = plt.subplots(1, 2, figsize = (16,8))
#     ax3.axis([xmin,xmax,ymin,ymax])
#     ax4.axis([xmin2,xmax2,ymin2,ymax2])
# plt.ion()
# 
# 
# """ C. CONTINUOUS DATA TRACKING """
# 
# if second_loop == True:
#     while True:      
#         if index>=20:
#             ser.reset_input_buffer()
#             ser.reset_output_buffer()
#         ser.reset_input_buffer()
#         ser.reset_output_buffer()
#         
#         c = ser.readline()
#         c = (str(c)[2:-5])
#         c = c.split(delimiter)
#         
#         try:
#             a = [float(i) for i in c]
#         except ValueError:
#             try:
#                 a = a
#             except NameError:
#                 if sensor_num == 2:
#                     a = [0.1,0.1]
#                 elif sensor_num == 3:
#                     a = [0.1,0.1,0.1]
#                 elif sensor_num == 4:
#                     a = [0.1,0.1,0.1,0.1]
#                     
#         if sensor_num == 4:
#             if ((len(a) == 4)):
#                 x0 = float(a[0])
#                 x1 = float(a[1])
#                 x2 = float(a[2])
#                 x3 = float(a[3])
#                 
#                 m1 = (x1 - centres[0][1])/(x0 - centres[0][0])
#                 m2 = (x3 - centres[0][3])/(x0 - centres[0][2])
#                 b1 =( x1 - m1*x0 )
#                 b2 = (x3 - m2*x2)
#                 
#                 for i in range(motion_num):
#                     probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[m1],[0],[0],[b1],[m2],[0],[0],[b2]]))))
#                 if distance([x0,x1,x2,x3],[centres[0][0], centres[0][1], centres[0][2], centres[0][3]]) > 2: 
#                     cluster_num = np.argmax(probabilities)
#                 else:
#                     cluster_num = 0
#                 
#                 ax3.scatter(x0,x1,s=50, color = colors[cluster_num])
#                 ax4.scatter(x2,x3,s=50, color = colors[cluster_num])
#                 plt.pause(0.0000001)
#                 ax3.clear()
#                 ax4.clear()
#                 ax3.axis([xmin,xmax,ymin,ymax])
#                 ax4.axis([xmin2,xmax2,ymin2,ymax2])
#         
#         elif sensor_num == 3:
#             if ((len(a) == 3)):
#                 x = float(a[0])
#                 y = float(a[1])
#                 z = float(a[2])
#                 
#                 if converted:
#                     converted_xyz = threeDconv([[x],[y],[z]])
#                     x = converted_xyz[0][0]
#                     y = converted_xyz[1][0]
#                     z = converted_xyz[2][0]
#                     
#                 for i in range(motion_num):
#                     probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x],[y],[z]]))))
#                 
#                 cluster_num = np.argmax(probabilities)
#                 
#                 ax.scatter(x,y,z,s=40, c = colors[cluster_num])
#                 plt.pause(0.00001)
#                 ax.clear()
#                 ax = plt.axes(projection = "3d")
#                 ax.set_xlim(xmin,xmax)
#                 ax.set_ylim(ymin,ymax)
#                 ax.set_zlim(zmin,zmax)
#                 
#                 
#     
#         elif sensor_num == 2:
#             if ((len(a) == 2)):
#                 x = float(a[0])
#                 y = float(a[1])
# 
#                 for i in range(motion_num):
#                     probabilities.append(sigmoid(np.dot(np.array([optimal_theta[i]]),np.array([[x],[y]]))))
#                 
#                 cluster_num = np.argmax(probabilities)
#                
#                 plt.scatter(x,y,s=40, c = colors[cluster_num])
#                 plt.pause(0.00001)
#                 plt.clf()
#                 plt.axis([xmin,xmax,ymin,ymax])
# 
# 
#                     
#                         
#         line = []
#         probabilities = []
# 
# 
# ser.close()
