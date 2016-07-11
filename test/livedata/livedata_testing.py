#importing libraries
import serial
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = plt.axes(projection='3d')
import random
import numpy as np
import skfuzzy as fuzz
import time
from matplotlib import animation


fig = plt.figure(2)
ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
scat = ax.scatter([], [])

def animate(i):
    ax.scatter(val_a[:i], val_b[:i])
    return scat

#this will store the line
line = []
vallist = []
val_a = []
val_b = []
val_c = []
colors = ['g', 'm', 'b', 'r', 'c', 'y', 'k', 'Brown', 'ForestGreen']
#plt.ion
plt.axis([0,100,0,100])

time1 = time.time()
index = 0
while index<5:
    
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    #anim = animation.FuncAnimation(fig, animate, frames=100, 
                            #interval=0.01, blit=False, repeat=False)
    plt.scatter(val_a[-1], val_b[-1], s=10, color = "y")
    
    #ax.scatter(val_a[-1], val_b[-1],val_c[-1])
    index += 1
    #insert the timing
    plt.pause(0.00000000000001)

time2 = time.time()
print (200/(time2-time1))


#while True:
    #insert the timing
    #plt.pause(0.1)
alldata = [val_a,val_b]
alldata = np.asarray(alldata)
print (alldata)
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, 4, 2, error=0.0005, maxiter=10000, init=None, seed=None)
print(u)
cluster_membership = np.argmax(u, axis=0)
for j in range(4):
    for i in range(len(cluster_membership)):
        if cluster_membership[i] == j:
            plt.plot(val_a[i], val_b[i], '.', color = colors[j])
    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")


#v = fuzz.cluster.cmeans_predict(alldata, cntr, 2, error = 0.0005, maxiter = 10000)
#print("hi")
#print(v[0])
#print(v[0] == u)
#cluster_membership2 = np.argmax(v[0], axis=0)
#print(cluster_membership2)


for point in cntr:
    for point2 in cntr:
        plt.plot([point[0], point2[0]], [point[1], point2[1]],"-b")

plt.savefig('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\figures\\test3.png')
  
        
plt.clf()
plt.axis([0,100,0,100])
for j in range(4):              #change value to match clusters
    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")


index = 0
x = []
y = []
currentarray = []
while index<1000:
    
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    
    if index<=10:
        a = np.asarray([[val_a[-1]], [val_b[-1]]])
        v = fuzz.cluster.cmeans_predict(a, cntr, 2, error = 0.0005, maxiter = 10000)
        cluster_num = np.argmax(v[0], axis = 0)
        cluster_num = int(cluster_num)
        plt.scatter(val_a[-1], val_b[-1], s=10, color = colors[cluster_num])
        #ax.scatter(val_a[-1], val_b[-1],val_c[-1])
        index += 1
        #insert the timing
        plt.pause(0.00000000000001)
        currentarray.append([val_a[-1], val_b[-1]])
    if index>10:
        plt.clf()
        plt.axis([0,100,0,100])
        for j in range(4):              #change value to match clusters
            plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
            currentarray[index%5] = ([val_a[-1], val_b[-1]])
        for i in currentarray:
            #plt.scatter(i[0],i[1], s=10, color = "y")
            a = np.asarray([[i[0]], [i[1]]])
            v = fuzz.cluster.cmeans_predict(a, cntr, 2, error = 0.0005, maxiter = 10000)
            cluster_num = np.argmax(v[0], axis = 0)
            cluster_num = int(cluster_num)
            plt.scatter(i[0], i[1], s=10, color = colors[cluster_num])
        plt.pause(0.0001)
        index += 1
"""        
while index<50:
    
    val_a.append(random.randint(0,100))
    val_b.append(random.randint(0,100))
    val_c.append(random.randint(0,100))
    plt.scatter(val_a[-1], val_b[-1], s=10, color = "y")
    
    #ax.scatter(val_a[-1], val_b[-1],val_c[-1])
    index += 1
    #insert the timing
    plt.pause(0.00000000000001)
    if index%5 == 0:
        plt.clf()
        ax.clear()
        plt.axis([0,100,0,100])
        for j in range(4):              #change value to match clusters
            plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")
            plt.scatter([1,2,3,4],[3,4,5,6])

time2 = time.time()
print (200/(time2-time1))
   
    
    
    #print one at a time
    
    #plt.clf()
    #plt.axis([0,100,0,100])
    #for j in range(4):              #change value to match clusters
    #    plt.plot(cntr[j][0], cntr[j][1], colors[j]+"s")

time2 = time.time()
print (200/(time2-time1))
"""