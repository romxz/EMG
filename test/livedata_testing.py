#importing libraries
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = plt.axes(projection='3d')
import random

#this will store the line
line = []
vallist = []
val_a = []
val_b = []
val_c = []

#plt.ion
#plt.axis([0,100,0,100])

index = 0
while index<50:
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    ax.scatter(val_a[-1], val_b[-1],val_c[-1])
    index += 1
    #insert the timing
    plt.pause(0.1)

#while True:
    #insert the timing
    #plt.pause(0.1)