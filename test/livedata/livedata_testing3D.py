#importing libraries
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(0)
ax = plt.axes(projection='3d')
import random
import numpy as np
import skfuzzy as fuzz

#this will store the line
line = []
vallist = []
val_a = []
val_b = []
val_c = []
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']
#plt.ion
#plt.axis([0,100,0,100])

index = 0
while index<10:
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    #plt.scatter(val_a[-1], val_b[-1], s=10, color = "y")
    ax.scatter(val_a[-1], val_b[-1],val_c[-1])
    print(val_a[-1])
    index += 1
    #insert the timing
    plt.pause(0.00000000000001)

ax = plt.axes(projection='3d')
alldata = [val_a,val_b,val_c]
alldata = np.asarray(alldata)
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 4, 2, error=0.0005, maxiter=10000, init=None, seed=None)
cluster_membership = np.argmax(u, axis=0)
print(cntr)
print(cntr[1][0])
for j in range(4):
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            ax.scatter(val_a[i], val_b[i], val_c[i],c = colors[j], s = 20, marker = "o")
            print("hi")
    ax.scatter(cntr[j][0], cntr[j][1], cntr[j][2], c = colors[j], marker = "s", s = 50)

for point in cntr:
   for point2 in cntr:
       ax.plot([point[0], point2[0]], [point[1], point2[1]], [point[2], point2[2]],"-b")
print(cntr)

fig1 = plt.figure(1)
ax = plt.axes(projection='3d')
index = 0
while True:
    plt.clf()
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    #plt.scatter(val_a[-1], val_b[-1], s=10, color = "y")
    ax.scatter(val_a[-1], val_b[-1],val_c[-1])
    print(val_a[-1])
    index += 1
    #insert the timing
    plt.pause(0.00000000000001)